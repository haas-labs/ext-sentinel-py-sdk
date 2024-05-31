import multiprocessing as mp
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List

from sentinel.metrics.core import MetricQueue
from sentinel.models.sentry import Sentry
from sentinel.models.settings import Settings
from sentinel.sentry.core import CoreSentry
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import logger
from sentinel.version import VERSION


@dataclass
class SentryInstance:
    settings: Sentry
    pid: int = None
    name: str = None
    restart: bool = None
    instance: CoreSentry = None
    schedule: str = None
    launch_time: datetime = None
    status: str = None
    exitcode: int = None


# Constants

STATE_CHECK_TIME_INTERVAL = 30
TERMINATION_TIMEOUT = 3


class Dispatcher:
    def __init__(self, settings: Settings) -> None:
        mp.set_start_method("spawn", force=True)

        self.settings = settings
        self.project = settings.project

        # Change dispatcher name for logging
        dispatcher = mp.current_process()
        dispatcher.name = "Dispatcher"

        logger.info(f"Sentinel SDK version: {VERSION}")

        self.metrics = None
        self.activate_monitoring()

        # prepare the list of sentries for launch
        self._sentry_instances: List[SentryInstance] = self.sentry_instances_from_settings()

    def sentry_instances_from_settings(self) -> List[SentryInstance]:
        instances = []
        for s in self.settings.sentries:
            if s.restart and s.schedule is not None:
                logger.warning(
                    f"The restart option will be unavailable while the schedule is active, sentry: {s.name} "
                )
                s.restart = False
            instance = SentryInstance(settings=s, name=s.name, restart=s.restart, schedule=s.schedule)
            instances.append(instance)
        return instances

    @property
    def active_sentries(self):
        return [s for s in self._sentry_instances if s.instance is not None and s.instance.is_alive()]

    @property
    def restarting_sentries(self):
        return [s for s in self._sentry_instances if s.restart]

    @property
    def scheduled_sentries(self):
        print(self._sentry_instances)
        return [s for s in self._sentry_instances if s.schedule is not None]

    @property
    def processing_completed(self):
        """
        returns processing completed status
        - True: if at least on active/restarted/scheduled sentries are running
        - False: no sentries for processing or initial state, before dispatcher run
        """
        return (
            True
            if (
                len(self.active_sentries) == 0
                and len(self.restarting_sentries) == 0
                and len(self.scheduled_sentries) == 0
            )
            else False
        )

    def activate_monitoring(self):
        """
        Activate monitoring if project.config.monitoring_enabled is True
        """
        monitoring_enabled = self.project.config.monitoring_enabled
        monitoring_port = self.project.config.monitoring_port
        if not monitoring_enabled:
            return

        logger.info(f"Enabling monitoring, metric server port: {monitoring_port}")
        self.metrics = MetricQueue()
        self.settings.sentries.append(
            Sentry(
                name="MetricServer",
                type="sentinel.sentry.metric.MetricServer",
                parameters={"port": monitoring_port},
                restart=True,
            )
        )

    def _log_intro(self):
        """
        Show project details in log
        """
        logger.info(
            "Project: {}".format(
                {
                    "name": self.settings.project.name if self.settings.project else "Unknown",
                    "description": self.settings.project.description if self.settings.project else "",
                }
            )
        )

    def _log_sentries_stats(self) -> None:
        logger.info(
            "Sentries: "
            + f"{len(self._sentry_instances)} total, "
            + f"{len(self.active_sentries)} active, "
            + f"{len(self.restarting_sentries)} restarting, "
            + f"{len(self.scheduled_sentries)} scheduled, "
            + f"{len(self._sentry_instances) - len(self.active_sentries)} finished"
        )

    def run_sentry(self, sentry: SentryInstance) -> SentryInstance:
        """
        Run sentry and update sentry instance details
        """
        settings = sentry.settings
        # Sentry init
        try:
            _, sentry_class = import_by_classpath(settings.type)
            sentry.instance = sentry_class(
                name=settings.name,
                description=settings.description,
                restart=settings.restart,
                parameters=settings.parameters,
                inputs=settings.inputs,
                outputs=settings.outputs,
                databases=settings.databases,
                metrics=self.metrics,
                schedule=settings.schedule,
                settings=self.settings,
            )
        except RuntimeError as err:
            logger.error(f"{settings.type} initialization issue, {err}")
            return None

        if settings.schedule:
            current_datetime = datetime.now(tz=timezone.utc).replace(second=0).replace(microsecond=0)
            time_to_run = sentry.instance.time_to_run()
            # logger.info(
            #     f"Time to run: {time_to_run['curr_date']}, last launch time: {sentry.launch_time}, current datetime: {current_datetime}"
            # )
            if time_to_run["curr_date"] == sentry.launch_time or time_to_run["curr_date"] != current_datetime:
                return sentry
            sentry.instance.run_on_schedule = True

        sentry.instance.start()
        sentry.launch_time = datetime.now(tz=timezone.utc).replace(microsecond=0).replace(second=0)
        return self.update_senty_instance_opts(sentry)

    def update_senty_instance_opts(self) -> None:
        for _id, sentry in enumerate(self._sentry_instances):
            # ignore active and running instances
            if sentry.instance is not None and sentry.instance.is_alive():
                continue

            # sentry.name = sentry.settings.name
            # sentry.restart = sentry.settings.restart
            # sentry.schedule = sentry.settings.schedule

            if sentry.instance is not None:
                sentry.pid = sentry.instance.pid
                if sentry.instance.is_alive():
                    sentry.status = "started"
                else:
                    sentry.status = "stopped"
                    sentry.exitcode = sentry.instance.exitcode
                    sentry.instance = None

            self._sentry_instances[_id] = sentry

    def _rerun_inactive_sentries(self):
        for _id, sentry in enumerate(self._sentry_instances):
            # ignore running sentries
            if sentry.instance is not None:
                continue

            # ignore finished sentries w/o restart flag = true
            if sentry.status == "stopped" and not sentry.restart and not sentry.schedule:
                continue

            if sentry.status == "stopped" and sentry.restart:
                logger.warning(f"Detected inactive sentry ({sentry.name}), restarting...")

            self._sentry_instances[_id] = self.run_sentry(sentry)

    def run(self) -> None:
        self._log_intro()

        try:
            while True:
                self._rerun_inactive_sentries()
                self._log_sentries_stats()

                # update instance options for finished sentry(-ies)
                self.update_senty_instance_opts()

                # Stop processing if no active sentries
                if self.processing_completed:
                    logger.info("No active sentries")
                    break

                time.sleep(STATE_CHECK_TIME_INTERVAL)

        except KeyboardInterrupt:
            logger.warning("Interrupting by user")
        finally:
            self.stop()

    def stop(self):
        # Terminate the rest of sentries
        for sentry in self.active_sentries:
            if sentry is not None and sentry.instance.is_alive():
                logger.info(f"Terminating the sentry: {sentry.name}")
                sentry.instance.terminate()

        # Make sure that sentry instance terminated
        while True:
            active_sentries = [s.instance.logger_name for s in self.active_sentries]
            if len(active_sentries) == 0:
                break
            logger.info(f"Waiting for termination, {active_sentries}")
            time.sleep(TERMINATION_TIMEOUT)
        logger.info("Termination completed")
