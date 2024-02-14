import asyncio
import logging

import multiprocessing as mp

from collections import Counter
from typing import Dict, List, Any

from sentinel.models.transaction import Transaction


logger = logging.getLogger(__name__)


class Process(mp.Process):
    """
    Sentinel Process
    """

    def __init__(
        self,
        name: str,
        description: str,
        parameters: Dict,
        inputs: List,
        outputs: List,
        databases: List,
    ) -> None:
        """
        Sentinel Process Init
        """
        super().__init__()

        self.name = name
        self.description = description
        self.parameters = parameters

        self.metrics = Counter()

        self.channels = dict()
        self.databases = dict()

        self.init_databases(databases)
        self.init_channels(inputs, outputs)

    def init_databases(self, databases: Dict) -> None:
        """
        Init databases
        """
        self.databases = {}
        for db_name, db in databases.items():
            self.databases[db_name] = db.instance

    def init_channels(self, inputs: Dict, outputs: Dict) -> None:
        """
        Init input/output channels
        """
        self.channels = {}
        for ch_name, channel in inputs.items():
            self.channels[ch_name] = channel.instance
            self.channels[ch_name].on_message = self.on_message

        for ch_name, channel in outputs.items():
            self.channels[ch_name] = channel.instance

    async def _run(self) -> None:
        """
        Run Process
        """
        try:
            channels = []
            for name, channel in self.channels.items():
                logger.info(f"Starting channel, name: {name}")
                channel_task = asyncio.create_task(channel.run(), name=name)
                channels.append(channel_task)
            await asyncio.gather(*channels)
        finally:
            logger.info("Processor completed")

    def run(self, **kwargs):
        """
        Run Process
        """
        asyncio.run(self._run())

    async def on_message(self, msg: Any) -> None:
        """
        Hook on incoming message
        """
        pass


class Detector(mp.Process):
    """
    Detector
    """

    def __init__(
        self,
        name: str,
        description: str,
        inputs: Dict,
        outputs: Dict,
        databases: Dict,
        parameters: Dict,
    ) -> None:
        """
        Detector Init
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
                self.channels[
                    "transactions"
                ].on_transactions_batch = self.on_transactions_batch

        for ch_name, channel in outputs.items():
            # Setup events channel if specified
            if channel.name == "events":
                self.channels["events"] = channel.instance

        self.transactions_batch_size = self.parameters.get("batch_size", 100)

    async def _run(self) -> None:
        """
        Run Detector processing
        """
        try:
            channels = []
            for name, channel in self.channels.items():
                logger.info(f"Starting channel, name: {name}")
                channel_task = asyncio.create_task(channel.run(), name=name)
                channels.append(channel_task)
            await asyncio.gather(*channels)
        finally:
            logger.info("Detector Processing completed")

    def run(self, **kwargs):
        """
        Run Detector processing
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

    async def on_transactions_batch(self, transactions: List[Transaction]) -> None:
        """
        Handle Transactions
        """
        pass
