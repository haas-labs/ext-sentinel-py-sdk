import time

from pathlib import Path

from sentinel.models.transaction import Transaction
from sentinel.channels.fs.common import InboundFileChannel


class TransactionsChannel(InboundFileChannel):
    """
    Inbound Transactions File Channel
    """

    def __init__(
        self, name: str, path: Path, use_current_time: bool = False, **kwargs
    ) -> None:
        """
        Inbound Transaction File Channel Init
        """
        super().__init__(
            name, "sentinel.models.transaction.Transaction", path, **kwargs
        )
        self.use_current_time = use_current_time

    async def on_message(self, message: Transaction) -> None:
        """
        Handle consumer message for transaction channel
        """
        if self.use_current_time:
            message.block.timestamp = int(time.time())
        await self.on_transaction(message)

        # TODO add handling of transactions batch

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        pass
