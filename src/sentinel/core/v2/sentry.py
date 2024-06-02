import asyncio
import logging
import multiprocessing
from datetime import datetime, timezone
from typing import Dict, List

from croniter import croniter

# from sentinel.core.v2.channel import SentryInputs, SentryOutputs
# from sentinel.core.v2.db import SentryDatabases
from sentinel.core.v2.handler import Handler
from sentinel.metrics.core import MetricQueue
from sentinel.metrics.registry import Registry
from sentinel.models.sentry import Sentry
from sentinel.utils.logger import get_logger


class CoreSentry(multiprocessing.Process):
    """
    Core Sentry is main processing unit in Sentinel.
    Used for building new type of sentries or as one run processing
    """

    # `name` is the sentry name. By default, a unique name is constructed of
    # the form “Sentry-N” where N is a small decimal number
    name: str = "CoreSentry"

    # `description` is the sentry descritpion. By default, short description to help
    # understand sentry's purpose
    description: str = "Core Sentry"

    def __init__(
        self,
        name: str = None,
        description: str = None,
        restart: bool = True,
        parameters: Dict = dict(),
        schedule: str = None,
        **kwargs,
    ) -> None:
        """
        The parent process starts a fresh Python interpreter process. The child process will
        only inherit those resources necessary to run the process object’s run() method.
        In particular, unnecessary file descriptors and handles from the parent process will
        not be inherited
        """
        super().__init__()

        # if name is not specified, use predefined one
        self.name = name if name is not None else self.name

        self.logger_name = self.name

        # if description is not specified, use predefined one
        self.description = (
            description.strip() if description is not None else " ".join(self.description.split()).strip()
        )
        self.restart = restart

        self.parameters = parameters.copy()

        self.schedule = schedule
        self.run_on_schedule = False
        self.kwargs = kwargs

    @classmethod
    def from_settings(cls, settings: Sentry):
        # inputs=settings.inputs,
        # outputs=settings.outputs,
        # databases=settings.databases,
        # metrics=self.metrics,

        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            parameters=settings.parameters,
            schedule=settings.schedule,
        )

    def run(self) -> None:
        """
        Method representing sentry's activity
        """
        self.init()
        self.on_init()
        if self.run_on_schedule:
            self.on_schedule()
        self.on_run()

    def init(self) -> None:
        self.logger = get_logger(name=self.logger_name, log_level=self.parameters.get("log_level", logging.INFO))

    def time_to_run(self) -> datetime:
        if self.schedule is None:
            return False
        cron = croniter(self.schedule, datetime.now(tz=timezone.utc))
        return {
            "prev_date": cron.get_prev(datetime),
            "curr_date": cron.get_current(datetime),
            "next_date": cron.get_next(datetime),
        }

    def on_init(self) -> None: ...

    def on_run(self) -> None: ...

    def on_schedule(self) -> None: ...


class AsyncCoreSentry(CoreSentry):
    name = "AsyncCoreSentry"
    description = "Async Core Sentry"

    def __init__(
        self,
        name: str = None,
        description: str = None,
        handlers: List[Handler] = list(),
        parameters: Dict = dict(),
        restart: bool = True,
        metrics: MetricQueue = None,
        schedule: str = None,
        **kwargs,
    ) -> None:
        super().__init__(
            nmae=name, description=description, restart=restart, parameters=parameters, schedule=schedule, **kwargs
        )

        self.handlers = handlers
        self.metrics = None
        self.metrics_queue = metrics

    def init(self) -> None:
        super().init()

        # self.inputs = SentryInputs(
        #     sentry_name=self.name,
        #     ids=self._inputs,
        #     channels=self.settings.inputs if hasattr(self.settings, "inputs") else [],
        # )
        # self.outputs = SentryOutputs(
        #     ids=self._outputs, channels=self.settings.outputs if hasattr(self.settings, "outputs") else []
        # )
        # self.databases = SentryDatabases(
        #     ids=self._databases, databases=self.settings.databases if hasattr(self.settings, "databases") else []
        # )
        if self.metrics_queue is not None:
            self.metrics = Registry()

    async def _run(self) -> None:
        """
        Sentry processing itself
        """
        await self.on_init()

        try:
            self.logger.info(f"Starting sentry process, {self.name}")

            # TODO extend this method with required async activities
            # await asyncio.gather(*activities)
        finally:
            self.logger.info("Processing completed")

    def run(self) -> None:
        """
        Method representing async sentry's activity
        """
        self.init()

        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")

    async def on_init(self) -> None: ...

    async def on_run(self) -> None: ...
