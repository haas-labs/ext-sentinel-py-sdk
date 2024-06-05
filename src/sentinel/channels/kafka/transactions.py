from aiokafka.structs import ConsumerRecord
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.channel import Channel
from sentinel.models.transaction import Transaction
from sentinel.transform import json_deserializer


class InboundTransactionsChannel(InboundKafkaChannel):
    name = "transactions"

    def __init__(self, name: str, **kwargs) -> None:
        # Building sentry specific group id
        sentry_name = kwargs.pop("sentry_name")
        default_group_id = "sentinel.{}.tx".format(sentry_name)

        super().__init__(name, record_type="sentinel.models.transaction.Transaction", **kwargs)

        self.config["group_id"] = self.config.get("group_id", default_group_id)
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
