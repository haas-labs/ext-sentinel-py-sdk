from aiokafka.structs import ConsumerRecord

from sentinel.channels.kafka.common import json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.chains.vechain.transaction import VeChainTransaction
from sentinel.models.channel import Channel
from sentinel.models.transaction import Transaction


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
