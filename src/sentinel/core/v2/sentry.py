import asyncio
import logging
import multiprocessing
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict

from croniter import croniter
from sentinel.channels.metric.core import OutboundMetricChannel
from sentinel.core.v2.channel import Channels
from sentinel.core.v2.db import Databases
from sentinel.core.v2.handler import FlowType
from sentinel.core.v2.settings import Settings
from sentinel.metrics.core import MetricQueue
from sentinel.metrics.registry import Registry
from sentinel.models.sentry import Sentry
from sentinel.utils.logger import get_logger


@dataclass
class ScheduleDates:
    previous: datetime
    current: datetime
    next: datetime


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
        settings: Settings = Settings(),
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
        self.settings = settings

        self.databases = None

        self.schedule = schedule

        # TODO add handling of run_on_schedule flag
        self.run_on_schedule = False

        self.kwargs = kwargs

    @classmethod
    def from_settings(cls, settings: Sentry, **kwargs):
        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            parameters=settings.parameters,
            schedule=settings.schedule,
            settings=settings,
            **kwargs,
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
        self.databases = Databases(self.settings.databases)

    def time_to_run(self) -> ScheduleDates:
        if self.schedule is None:
            return None
        cron = croniter(self.schedule, datetime.now(tz=timezone.utc))
        return ScheduleDates(
            previous=cron.get_prev(datetime), current=cron.get_current(datetime), next=cron.get_next(datetime)
        )

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
        restart: bool = True,
        schedule: str = None,
        parameters: Dict = dict(),
        metrics_queue: MetricQueue = None,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        super().__init__(
            nmae=name, description=description, restart=restart, parameters=parameters, schedule=schedule, **kwargs
        )

        self._metrics_registry = None
        self._metrics_channel = None
        self._metrics_queue = metrics_queue
        self.settings = settings
        self.kwargs = kwargs

    @classmethod
    def from_settings(cls, settings: Sentry, metrics_queue: MetricQueue, **kwargs):
        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            schedule=settings.schedule,
            parameters=settings.parameters,
            metrics_queue=metrics_queue,
            settings=settings,
            **kwargs,
        )

    @property
    def metrics(self) -> Registry:
        return self._metrics_registry

    def init(self) -> None:
        super().init()

        # Metrics
        if self._metrics_queue is not None:
            self._metrics_registry = Registry()
            self.logger.info("Starting channel, name: metrics")
            self._metrics_channel = OutboundMetricChannel(
                id="metrics/publisher", queue=self._metrics_queue, registry=self.metrics
            )

        # Inputs
        for input in self.settings.inputs:
            input.flow_type = FlowType.inbound
        self.inputs = Channels(channels=self.settings.inputs, logger=self.logger, sentry_name=self.name)

        # Outputs
        for output in self.settings.outputs:
            output.flow_type = FlowType.outbound
        self.outputs = Channels(channels=self.settings.outputs, logger=self.logger, sentry_name=self.name)

    async def processing(self) -> None:
        """
        Sentry processing itself
        """
        await self.on_init()
        handlers = list()
        try:
            self.logger.info(f"Starting sentry process, name: {self.name}")
            for input in self.inputs:
                channel_handler = asyncio.create_task(input.run(), name=input.name)
                handlers.append(channel_handler)
            for output in self.outputs:
                channel_handler = asyncio.create_task(output.run(), name=output.name)
                handlers.append(channel_handler)
            if self._metrics_channel is not None:
                metrics_handler = asyncio.create_task(self._metrics_channel.run(), name=self._metrics_channel.name)
                handlers.append(metrics_handler)

            await asyncio.gather(*handlers)
        finally:
            self.logger.info("Processing completed")

    def run(self) -> None:
        """
        Method representing async sentry's activity
        """
        self.init()

        try:
            asyncio.run(self.processing())
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")

    async def on_init(self) -> None: ...

    async def on_run(self) -> None: ...
