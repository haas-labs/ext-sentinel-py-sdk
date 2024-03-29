import time
import multiprocessing as mp

from typing import Any, Dict, List
from datetime import datetime, timezone

from dataclasses import dataclass

from sentinel.version import VERSION

from sentinel.profile import Profile
from sentinel.project import ProjectSettings

from sentinel.utils.logger import logger
from sentinel.models.sentry import Sentry
from sentinel.sentry.core import CoreSentry
from sentinel.utils.imports import import_by_classpath


@dataclass
class SentryInstance:
    settings: Sentry
    name: str = None
    pid: int = None
    restart: bool = None
    instance: CoreSentry = None
    schedule: str = None
    launch_time: datetime = None
    status: str = None
    exitcode: int = None


def process_init(process_classpath: str, **kwargs) -> Any:
    """
    start process
    """
    _, process_class = import_by_classpath(process_classpath)
    logger.info(f"Importing {process_class}")
    return process_class(**kwargs)


# Constants

PROCESS_STATE_CHECK_TIME_INTERVAL = 30
STATE_CHECK_TIME_INTERVAL = 5
TERMINATION_TIMEOUT = 3


class Dispatcher:
    """
    Processes Dispatcher
    """

    def __init__(self, profile: Profile) -> None:
        """
        Processes Distpatcher
        """
        self._profile = profile
        self._processes = dict()

        dispatcher_process = mp.current_process()
        dispatcher_process.name = "Dispatcher"

        logger.info(f"Sentinel SDK version: {VERSION}")

    @property
    def processes(self):
        """
        returns processes
        """
        return self._processes

    def init(self):
        """
        Init components from profile
        """
        try:
            for process in self._profile.processes:
                # Channels
                input_channels = dict()
                for channel in process.inputs:
                    input_channels[channel.name] = channel
                    input_channels[channel.name].instance = self.init_channel(
                        ch_name=channel.name,
                        ch_type=channel.type,
                        ch_parameters=channel.parameters,
                    )
                output_channels = dict()
                for channel in process.outputs:
                    output_channels[channel.name] = channel
                    output_channels[channel.name].instance = self.init_channel(
                        ch_name=channel.name,
                        ch_type=channel.type,
                        ch_parameters=channel.parameters,
                    )
                # Databases
                databases = dict()
                for db in process.databases:
                    databases[db.name] = db
                    databases[db.name].instance = self.init_database(
                        db_name=db.name, db_type=db.type, db_parameters=db.parameters
                    )

                self._processes[process.name] = process
                self._processes[process.name].instance = self.init_process(
                    proc_name=process.name,
                    proc_type=process.type,
                    proc_descr=process.description,
                    proc_parameters=process.parameters,
                    inputs=input_channels,
                    outputs=output_channels,
                    databases=databases,
                )
        except RuntimeError as err:
            logger.error(f"Initialization failed, {err}")
            return False
        return True

    def init_database(self, db_name: str, db_type: str, db_parameters: Dict) -> Any:
        """
        Init database
        """
        db_instance = None
        try:
            logger.info(f"Initializing database: {db_name}, type: {db_type}")
            _, db_class = import_by_classpath(db_type)
            parameters = db_parameters if db_parameters is not None else {}
            db_instance = db_class(**parameters)
        except RuntimeError as err:
            logger.error(f"Database initialization issue, {err}")
            return None

        return db_instance

    def init_channel(self, ch_name: str, ch_type: str, ch_parameters: Dict) -> Any:
        """
        Init channel
        """
        ch_instance = None
        try:
            logger.info(f"Initializing channel: {ch_name}, type: {ch_type}")
            _, ch_class = import_by_classpath(ch_type)
            # parameters = ch_parameters if ch_parameters is not None else {}
            ch_instance = ch_class(name=ch_name, **ch_parameters)
        except RuntimeError as err:
            logger.error(f"{ch_name} -> Channel initialization issue, {err}")
            return None

        return ch_instance

    def init_process(
        self,
        proc_name: str,
        proc_type: str,
        proc_descr: str,
        proc_parameters: Dict,
        inputs: Dict,
        outputs: Dict,
        databases: Dict,
    ) -> Any:
        """
        Init process
        """
        proc_instance = None

        try:
            logger.info(f"Initializing process: {proc_name}, type: {proc_type}")
            _, proc_class = import_by_classpath(proc_type)
            parameters = proc_parameters if proc_parameters is not None else {}
            proc_instance = proc_class(
                name=proc_name,
                description=proc_descr,
                inputs=inputs,
                outputs=outputs,
                databases=databases,
                parameters=parameters,
            )
        except RuntimeError as err:
            process = {
                "name": proc_name,
                "type": proc_type,
                "description": proc_descr,
            }
            logger.error(f"{proc_name} -> Process initialization issue, {err}, " + f"Process: {process}")
            return None

        return proc_instance

    def run(self) -> None:
        """
        Run dispatcher
        """
        # Init processes before start
        if not self.init():
            logger.error("Process initialization failed")
            return

        for _, process_settings in self._processes.items():
            process_settings.instance.start()

        try:
            # Main loop
            while True:
                active_processes = [p for p in self._processes.values() if p.instance.is_alive()]
                logger.info(f"Active processes: {[ap.instance.name for ap in active_processes]}")

                for name, process in self._processes.items():
                    if not process.instance.is_alive():
                        logger.warning(f"Detected inactive process ({name}), restarting...")
                        process.instance.start()

                time.sleep(PROCESS_STATE_CHECK_TIME_INTERVAL)

        except KeyboardInterrupt:
            logger.warning("Interrupting by user")
        finally:
            self.stop()

        logger.info("Completed")

    def stop(self):
        """
        Stop processing
        """
        for process_name, process_settings in self._processes.items():
            logger.info(f"Terminating the process: {process_name}")
            process_settings.instance.terminate()


class SentryDispatcher:
    def __init__(self, settings: ProjectSettings) -> None:
        mp.set_start_method("spawn", force=True)

        self.settings = settings

        # Change dispatcher name for logging
        dispatcher = mp.current_process()
        dispatcher.name = "Dispatcher"

        logger.info(f"Sentinel SDK version: {VERSION}")

        # prepare the list of sentries for launch
        self._sentry_instances: List[SentryInstance] = []
        for s in self.settings.sentries:
            if s.restart and s.schedule is not None:
                logger.warning(
                    f"The restart option will be unavailable while the schedule is active, sentry: {s.name} "
                )
                s.restart = False
            instance = SentryInstance(settings=s)
            self._sentry_instances.append(instance)

        # self._log_queue = mp.Queue()

    @property
    def active_sentries(self):
        return [s for s in self._sentry_instances if s.instance is not None and s.instance.is_alive()]

    @property
    def restarting_sentries(self):
        return [s for s in self._sentry_instances if s.restart]

    @property
    def scheduled_sentries(self):
        return [s for s in self._sentry_instances if s.schedule is not None]

    def intro(self):
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

    def update_senty_instance_opts(self, sentry: SentryInstance) -> SentryInstance:
        sentry.name = sentry.settings.name
        sentry.restart = sentry.settings.restart
        sentry.schedule = sentry.settings.schedule

        if sentry.instance is not None:
            sentry.pid = sentry.instance.pid
            if sentry.instance.is_alive():
                sentry.status = "started"
            else:
                sentry.status = "stopped"
                sentry.exitcode = sentry.instance.exitcode
                sentry.instance = None

        return sentry

    def run(self) -> None:
        self.intro()

        try:
            while True:
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

                logger.info(
                    "Sentries: "
                    + f"{len(self._sentry_instances)} total, "
                    + f"{len(self.active_sentries)} active, "
                    + f"{len(self.restarting_sentries)} restarting, "
                    + f"{len(self.scheduled_sentries)} scheduled, "
                    + f"{len(self._sentry_instances) - len(self.active_sentries)} finished"
                )

                # update instance options for finished sentry(-ies)
                for _id, sentry in enumerate(self._sentry_instances):
                    if sentry.instance is not None and sentry.instance.is_alive():
                        continue
                    self._sentry_instances[_id] = self.update_senty_instance_opts(sentry)

                # Stop processing if no active sentries
                if (
                    len(self.active_sentries) == 0
                    and len(self.restarting_sentries) == 0
                    and len(self.scheduled_sentries) == 0
                ):
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
