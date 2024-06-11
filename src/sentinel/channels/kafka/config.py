from aiokafka.structs import ConsumerRecord
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.channel import Channel
from sentinel.models.config import Configuration
from sentinel.transform import json_deserializer


class InboundConfigChannel(InboundKafkaChannel):
    name = "config"

    def __init__(self, name: str, **kwargs) -> None:
        sentry_name = kwargs.pop("sentry_name")
        network = kwargs.pop("network")
        default_group_id = f"sentinel.{network}.{sentry_name}.tx"

        super().__init__(name, record_type="sentinel.models.config.Configuration", **kwargs)

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
        key = int(message.key, 16)
        data = message.value
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
