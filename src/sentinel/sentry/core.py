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
        self.logger_name = self.name
        self.description = (
            description.strip() if description is not None else " ".join(self.description.split()).strip()
        )
        self.parameters = parameters.copy()
        self.settings = settings

        self._inputs = inputs
        self._outputs = outputs
        self._databases = databases

    def run(self) -> None:
        """
        Method representing sentry's activity
        """
        self.activate()
        self.on_init()
        self.on_run()

    def activate(self):
        """
        Activate Sentry periphery
        """
        self.logger = get_logger(name=self.logger_name, log_level=self.settings.settings.get("LOG_LEVEL", logging.INFO))

        self.inputs = SentryInputs(
            sentry_name=self.name,
            ids=self._inputs,
            channels=self.settings.inputs if hasattr(self.settings, "inputs") else [],
        )
        self.outputs = SentryOutputs(
            ids=self._outputs, channels=self.settings.outputs if hasattr(self.settings, "outputs") else []
        )
        self.databases = SentryDatabases(
            ids=self._databases, databases=self.settings.databases if hasattr(self.settings, "databases") else []
        )

    def on_init(self) -> None: ...

    def on_run(self) -> None: ...


class AsyncCoreSentry(CoreSentry):
    name = "AsyncCoreSentry"
    description = "Async Core Sentry"

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
        self.activate()
        
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")

    async def on_init(self) -> None: ...

    async def on_run(self) -> None: ...
