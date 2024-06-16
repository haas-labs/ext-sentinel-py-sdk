from aiokafka.structs import ConsumerRecord
from sentinel.channels.kafka.common import bytes2int_deserializer, json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.channel import Channel


class InboundConfigChannel(InboundKafkaChannel):
    name = "config"

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, record_type="sentinel.models.config.Configuration", **kwargs)

        self.config["group_id"] = self.config.get("group_id", f"sentinel.{self.sentry_name}.{self.sentry_hash}")
        self.config["key_deserializer"] = bytes2int_deserializer
        self.config["value_deserializer"] = json_deserializer
        self.config["auto_offset_reset"] = "earliest"

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
        await self.on_config_change(record=message)

    async def on_config_change(self, record: ConsumerRecord) -> None: ...
