import asyncio
import logging


import multiprocessing as mp

from typing import Dict
from collections import Counter

from sentinel.models.transaction import Transaction


logger = logging.getLogger(__name__)


class TransactionDetector(mp.Process):
    """
    Transaction Detector
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        inputs: Dict = dict(),
        outputs: Dict = dict(),
        databases: Dict = dict(),
        parameters: Dict = dict(),
    ) -> None:
        """
        Transaction Detector Init
        """
        super().__init__()

        # Process Name
        network = parameters.get("network", "")
        self.name = "@".join([network, name]) if network != "" else name

        # Detector Name
        self.detector_name = name

        self.description = description
        self.parameters = parameters

        self.metrics = Counter()

        # Databases
        self.databases = {}
        for db_name, db in databases.items():
            self.databases[db_name] = db.instance

        # Channels
        self.channels = {}
        for ch_name, channel in inputs.items():
            # Setup transactions channel if specified
            if ch_name == "transactions":
                self.channels["transactions"] = channel.instance
                self.channels["transactions"].on_transaction = self.on_transaction

        for ch_name, channel in outputs.items():
            # Setup events channel if specified
            if channel.name == "events":
                self.channels["events"] = channel.instance

    async def init(self) -> None:
        '''
        Detector specific initialization

        User can add custom init logic here
        '''
        pass

    async def _run(self) -> None:
        """
        Run Transaction Detector processing
        """
        await self.init()

        try:
            channels = []
            for name, channel in self.channels.items():
                logger.info(f"Starting channel, name: {name}")
                channel_task = asyncio.create_task(channel.run(), name=name)
                channels.append(channel_task)
            await asyncio.gather(*channels)
        finally:
            logger.info("Transaction Detector Processing completed")

    def run(self, **kwargs):
        """
        Run Transaction Detector processing
        """
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            logger.warning("Interrupted by user")

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        pass
