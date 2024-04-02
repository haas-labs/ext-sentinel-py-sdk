import asyncio
import platform

import multiprocessing as mp

from typing import Dict
from collections import Counter

from sentinel.definitions import BLOCKCHAIN
from sentinel.utils.logger import get_logger
from sentinel.models.transaction import Transaction

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
        self.logger = get_logger(__name__)

        if platform.system() == "Darwin":
            # TODO migrate a process to use spawn instead of fork
            # Current implementation is just workaround to solve issue on MacOS
            mp.set_start_method("fork", force=True)

        super().__init__()

        # Process Name
        network = parameters.get("network")
        assert network is not None, f"Unknown network, {network}"
        
        detector_prefix = BLOCKCHAIN.get(network).network
        self.name = "://".join([detector_prefix, name]) if network != "" else name

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
        """
        Detector specific initialization

        User can add custom init logic here
        """
        pass

    async def _run(self) -> None:
        """
        Run Transaction Detector processing
        """
        await self.init()

        try:
            channels = []
            for name, channel in self.channels.items():
                self.logger.info(f"Starting channel, name: {name}")
                channel_task = asyncio.create_task(channel.run(), name=name)
                channels.append(channel_task)
            await asyncio.gather(*channels)
        finally:
            self.logger.info("Transaction Detector Processing completed")

    def run(self, **kwargs):
        """
        Run Transaction Detector processing
        """
        try:
            asyncio.run(self._run())
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        pass
