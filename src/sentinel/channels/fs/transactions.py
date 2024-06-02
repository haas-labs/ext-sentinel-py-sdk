import time
from pathlib import Path

from sentinel.channels.fs.common import InboundFileChannel
from sentinel.core.v2.channel import ChannelModel
from sentinel.models.transaction import Transaction


class InboundTransactionsChannel(InboundFileChannel):
    name = "transactions"

    def __init__(self, name: str, path: Path, use_current_time: bool = False, **kwargs) -> None:
        super().__init__(name=name, record_type="sentinel.models.transaction.Transaction", path=path, **kwargs)
        self.use_current_time = use_current_time

    @classmethod
    def from_settings(cls, settings: ChannelModel, **kwargs):
        return cls(
            name=settings.name,
            path=settings.parameters.get("path"),
            use_current_time=settings.parameters.get("use_current_time"),
            **kwargs,
        )

    async def on_message(self, message: Transaction) -> None:
        """
        Handle consumer message for transaction channel
        """
        if self.use_current_time:
            message.block.timestamp = int(time.time() * 1000)
        await self.on_transaction(message)

        # TODO add handling of transactions batch

    async def on_transaction(self, transaction: Transaction) -> None: ...
