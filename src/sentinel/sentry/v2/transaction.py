from typing import Dict

from sentinel.core.v2.sentry import AsyncCoreSentry

# from sentinel.channels.metric.core import MetricChannel
from sentinel.core.v2.settings import Settings
from sentinel.definitions import BLOCKCHAIN
from sentinel.metrics.core import MetricQueue
from sentinel.models.transaction import Transaction

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
        schedule: str = None,
        parameters: Dict = dict(),
        metrics_queue: MetricQueue = None,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            schedule=schedule,
            parameters=parameters,
            metrics_queue=metrics_queue,
            settings=settings,
            **kwargs,
        )

        network = parameters.get("network")
        assert network is not None or network not in BLOCKCHAIN.keys(), f"Unknown network: {network}"

        detector_prefix = BLOCKCHAIN.get(network).network
        self.logger_name = "://".join([detector_prefix, self.name]) if network != "" else self.name

    def init(self) -> None:
        super().init()
        self.inputs.transactions.on_transaction = self.on_transaction

    # handle incoming transaction
    async def on_transaction(self, transaction: Transaction) -> None: ...
