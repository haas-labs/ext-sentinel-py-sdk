import hashlib

from aiokafka.structs import ConsumerRecord
from sentinel.channels.kafka.common import bytes2int_deserializer, json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.channel import Channel
from sentinel.models.config import Configuration


class InboundConfigChannel(InboundKafkaChannel):
    name = "config"

    def __init__(self, name: str, **kwargs) -> None:
        sentry_name = kwargs.pop("sentry_name")
        channel_hash = hashlib.sha256(str(id(self)).encode("utf-8")).hexdigest()[:6]
        default_group_id = f"sentinel.{sentry_name}.{channel_hash}"

        super().__init__(name, record_type="sentinel.models.config.Configuration", **kwargs)

        self.config["group_id"] = self.config.get("group_id", default_group_id)
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
        key = message.key
        data = message.value
        print(key, data)
        if data is not None:
            # remove unused fields to simplify configuration model
            data.pop("destinations", None)
            data.pop("actions", None)
        try:
            if data is not None:
                config: Configuration = self.record_type(**data)
            else:
                config = None
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_config_change(key=key, config=config)

    async def on_config_change(self, key: int, config: Configuration) -> None: ...
