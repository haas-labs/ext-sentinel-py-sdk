from typing import List

from aiokafka.structs import ConsumerRecord

from sentinel.transform import json_deserializer
from sentinel.models.transaction import Transaction
from sentinel.channels.kafka.inbound import InboundKafkaChannel


class InboundTransactionsChannel(InboundKafkaChannel):
    name = "transactions"

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, record_type="sentinel.models.transaction.Transaction", **kwargs)

        self.config["value_deserializer"] = json_deserializer

    async def on_message(self, message: ConsumerRecord) -> None:
        """
        Handle consumer message for transaction channel
        """
        data = message.value
        try:
            transaction: Transaction = self.record_type(**data)
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_transaction(transaction)

        # TODO add handling of transactions batch

    async def on_transaction(self, transaction: Transaction) -> None: ...

    async def on_transactions_batch(self, transactions: List[Transaction]) -> None: ...
