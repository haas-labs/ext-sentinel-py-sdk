from pathlib import Path

from sentinel.models.transaction import Transaction
from sentinel.channels.ws.common import InboundWebsocketChannel


class InboundTransactionsChannel(InboundWebsocketChannel):
    """
    Inbound Transactions Websocket Channel
    """

    def __init__(self, name: str, path: Path, use_current_time: bool = False, **kwargs) -> None:
        """
        Inbound Transaction Websocket Channel Init
        """
        super().__init__(name, "sentinel.models.transaction.Transaction", path, **kwargs)
        self.use_current_time = use_current_time

    async def on_message(self, message: Transaction) -> None:
        """
        Handle consumer message for transaction channel
        """
        await self.on_transaction(message)

        # TODO add handling of transactions batch

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        pass
