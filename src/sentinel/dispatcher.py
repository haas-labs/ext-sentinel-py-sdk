import time
import logging

from typing import Any, Dict

from sentinel.profile import Profile
from sentinel.utils.imports import import_by_classpath


logger = logging.getLogger(__name__)


def process_init(process_classpath: str, **kwargs) -> Any:
    """
    start process
    """
    _, process_class = import_by_classpath(process_classpath)
    logger.info(f"Importing {process_class}")
    return process_class(**kwargs)


# Constants

PROCESS_STATE_CHECK_TIME_INTERVAL = 30


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
