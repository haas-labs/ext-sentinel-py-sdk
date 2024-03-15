import asyncio
import logging
import multiprocessing

from typing import Dict


logger = logging.getLogger(__name__)


class CoreSentry(multiprocessing.Process):
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict = dict(),
    ) -> None:
        """
        - `name` is the sentry name. By default, a unique name is constructed of
          the form “Sentry-N” where N is a small decimal number
        - `description` is the sentry descritpion. By default, short description to help
          understand sentry's purpose
        - `args` is a list or tuple of arguments for the target invocation.
          Defaults to ()
        - `kwargs` is a dictionary of keyword arguments for the target invocation.
          Defaults to {}.
        """

        """
        The parent process starts a fresh Python interpreter process. The child process will 
        only inherit those resources necessary to run the process object’s run() method. 
        In particular, unnecessary file descriptors and handles from the parent process will 
        not be inherited
        """
        multiprocessing.set_start_method("spawn", force=True)

        super().__init__(name=name)
        self.description = description
        self.paramters = parameters

    def run(self) -> None:
        """
        Method representing sentry's activity
        """
        raise NotImplementedError()


class AsyncCoreSentry(CoreSentry):
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
        await self.init()

        try:
            logger.info(f"Starting sentry process, {self.name}")

            # TODO extend this method with required async activities
            # await asyncio.gather(*activities)
        finally:
            logger.info("Processor completed")

    def run(self) -> None:
        """
        Method representing async sentry's activity
        """
        asyncio.run(self._run())
