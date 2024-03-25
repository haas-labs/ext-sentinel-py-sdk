import asyncio
import logging
import multiprocessing

from typing import Dict, List

from sentinel.utils.logger import get_logger

from sentinel.models.project import ProjectSettings

from sentinel.sentry.db import SentryDatabases
from sentinel.sentry.channel import SentryInputs, SentryOutputs


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

    # Restart policy
    restart: bool = False

    def __init__(
        self,
        name: str = None,
        description: str = None,
        parameters: Dict = dict(),
        inputs: List[str] = list(),
        outputs: List[str] = list(),
        databases: List[str] = list(),
        settings: ProjectSettings = None,
    ) -> None:
        """
        The parent process starts a fresh Python interpreter process. The child process will
        only inherit those resources necessary to run the process object’s run() method.
        In particular, unnecessary file descriptors and handles from the parent process will
        not be inherited
        """
        super().__init__()
        self.name = name if name is not None else self.name
        self.description = (
            description.strip() if description is not None else " ".join(self.description.split()).strip()
        )
        self.parameters = parameters.copy()
        self.settings = settings
        self.inputs = SentryInputs(
            sentry_name=self.name, ids=inputs, channels=settings.inputs if hasattr(settings, "inputs") else []
        )
        self.outputs = SentryOutputs(ids=outputs, channels=settings.outputs if hasattr(settings, "outputs") else [])
        self.databases = SentryDatabases(
            ids=databases, databases=settings.databases if hasattr(settings, "databases") else []
        )

    def run(self) -> None:
        """
        Method representing sentry's activity
        """
        self.logger = get_logger(name=self.name, log_level=self.settings.settings.get("LOG_LEVEL", logging.INFO))
        self.on_init()
        self.on_run()

    def on_init(self) -> None: ...

    def on_run(self) -> None: ...


class AsyncCoreSentry(CoreSentry):
    name = "AsyncCoreSentry"
    description = "Async Core Sentry"

    async def init(self) -> None:
        """
        Sentry specific initialization. User can add custom init logic here. The logic which
        need to be applied before processing start
        """
        pass

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
        self.logger = get_logger(name=self.name, log_level=self.settings.settings.get("LOG_LEVEL", logging.INFO))
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")

    async def on_init(self) -> None: ...

    async def on_run(self) -> None: ...
