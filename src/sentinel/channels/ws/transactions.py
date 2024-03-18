from sentinel.models.transaction import Transaction
from sentinel.channels.ws.common import InboundWebsocketChannel


class InboundTransactionChannel(InboundWebsocketChannel):
    name = "transactions"

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, "sentinel.models.transaction.Transaction", **kwargs)

    async def on_message(self, message: Transaction) -> None:
        """
        Handle consumer message for transaction channel
        """
        await self.on_transaction(message)

        # TODO add handling of transactions batch

    async def on_transaction(self, transaction: Transaction) -> None: ...
