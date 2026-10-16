from aiokafka.structs import ConsumerRecord

from sentinel.channels.kafka.common import json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.chains.vechain.transaction import VeChainTransaction
from sentinel.models.channel import Channel
from sentinel.models.transaction import Transaction


def is_empty_block_placeholder(data) -> bool:
    """
    Check if a record is the placeholder the trunk ingest publishes for an empty block:
    no transaction hash and a block with zero transactions. It carries the block only
    and is not a real transaction.
    """
    if not isinstance(data, dict) or data.get("hash"):
        return False
    block = data.get("block")
    return isinstance(block, dict) and block.get("transaction_count") == 0


class InboundTransactionsChannel(InboundKafkaChannel):
    name = "transactions"

    def __init__(self, name: str, **kwargs) -> None:
        # Building sentry specific group id

        super().__init__(name, record_type="sentinel.models.transaction.Transaction", **kwargs)

        self.config["group_id"] = self.config.get("group_id", "sentinel.{}.tx".format(self.sentry_name))
        self.config["value_deserializer"] = json_deserializer

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            **kwargs,
        )

    async def on_message(self, message: ConsumerRecord) -> None:
        """
        Handle consumer message for transaction channel
        """
        data = message.value
        if is_empty_block_placeholder(data):
            self.logger.debug(
                f"{self.name} -> Skipping empty block placeholder, "
                f"block: {data['block'].get('number')}, offset: {message.offset}"
            )
            return
        try:
            transaction: Transaction = self.record_type(**data)
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_transaction(transaction)

    async def on_transaction(self, transaction: Transaction) -> None: ...


class InboundVeChainTransactionsChannel(InboundKafkaChannel):
    name = "transactions"

    def __init__(self, name: str, **kwargs) -> None:
        # Building sentry specific group id

        super().__init__(name, record_type="sentinel.models.chains.vechain.transaction.VeChainTransaction", **kwargs)

        self.config["group_id"] = self.config.get("group_id", "sentinel.{}.tx".format(self.sentry_name))
        self.config["value_deserializer"] = json_deserializer

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            **kwargs,
        )

    async def on_message(self, message: ConsumerRecord) -> None:
        """
        Handle consumer message for transaction channel
        """
        data = message.value
        try:
            transaction: VeChainTransaction = self.record_type(**data)
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_transaction(transaction)

    async def on_transaction(self, transaction: VeChainTransaction) -> None: ...
