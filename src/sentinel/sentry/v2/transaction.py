from typing import Dict

from sentinel.core.v2.sentry import AsyncCoreSentry

# from sentinel.channels.metric.core import MetricChannel
from sentinel.core.v2.settings import Settings
from sentinel.definitions import BLOCKCHAIN
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
        monitoring_enabled: bool = False,
        monitoring_port: int = 9090,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            schedule=schedule,
            parameters=parameters,
            monitoring_enabled=monitoring_enabled,
            monitoring_port=monitoring_port,
            settings=settings,
            **kwargs,
        )

        self.network = parameters.get("network")
        assert self.network is not None or self.network not in BLOCKCHAIN.keys(), f"Unknown network: {self.network}"

        detector_prefix = BLOCKCHAIN.get(self.network).network
        self.logger_name = "://".join([detector_prefix, self.name]) if self.network != "" else self.name

    def init(self) -> None:
        super().init()
        if getattr(self.inputs, "transactions", None):
            self.inputs.transactions.on_transaction = self.on_transaction
        else:
            raise AttributeError("Missed required transactions input channel, please check configuration")

    # handle incoming transaction
    async def on_transaction(self, transaction: Transaction) -> None: ...
