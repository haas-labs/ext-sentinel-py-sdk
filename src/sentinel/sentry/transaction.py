import asyncio

from typing import Dict, List

from sentinel.sentry.core import AsyncCoreSentry

from sentinel.definitions import BLOCKCHAIN

from sentinel.models.transaction import Transaction
from sentinel.models.project import ProjectSettings

"""
Transaction Detector uses for detection different cases in transaction stream.

The detector's dependencies (mandatory):
- inbound transaction channel
- outbound event channel

Optional dependencies:
- different databases

"""


class TransactionDetector(AsyncCoreSentry):
    name = "TransactionDetector"
    description = """
        The base detector which can be used for mointoring activities 
        in transactions stream and publishing results to events stream 
    """

    def __init__(
        self,
        name: str = None,
        description: str = None,
        restart: bool = True,
        parameters: Dict = dict(),
        inputs: List[str] = list(),
        outputs: List[str] = list(),
        databases: List[str] = list(),
        settings: ProjectSettings = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            parameters=parameters,
            inputs=inputs,
            outputs=outputs,
            databases=databases,
            settings=settings,
        )

        # remove empty spaces and new lines in description
        self.description = " ".join(self.description.split())

        network = parameters.get("network")
        assert network is not None, f"Unknown network, {network}"

        detector_prefix = BLOCKCHAIN.get(network).short_name
        self.logger_name = "://".join([detector_prefix, name]) if network != "" else name

    # handle incoming transaction
    async def on_transaction(self, transaction: Transaction) -> None: ...

    async def _run(self) -> None:
        """
        Run Transaction Detector processing
        """
        await self.on_init()

        try:
            channels = []
            # Inputs
            for name in self.inputs.channels:
                self.logger.info(f"Starting channel, name: {name}")
                channel_inst = getattr(self.inputs, name)
                if name == "transactions":
                    channel_inst.on_transaction = self.on_transaction
                channel_task = asyncio.create_task(channel_inst.run(), name=name)
                channels.append(channel_task)
            # Outputs
            for name in self.outputs.channels:
                self.logger.info(f"Starting channel, name: {name}")
                channel_inst = getattr(self.outputs, name)
                channel_task = asyncio.create_task(getattr(self.outputs, name).run(), name=name)
                channels.append(channel_task)
            await asyncio.gather(*channels)
        finally:
            self.logger.info("Transaction Detector Processing completed")
