from aiokafka.structs import ConsumerRecord

from sentinel.channels.kafka.common import json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.models.channel import Channel
from sentinel.models.chains.canton.update import CantonUpdate


class InboundCantonUpdatesChannel(InboundKafkaChannel):
    """
    Consumes CantonUpdate records from a tenant's topic (one topic per connected participant,
    e.g. canton.<tenant>.updates). The sentry binds `on_update`.
    """

    name = "updates"

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, record_type="sentinel.models.chains.canton.update.CantonUpdate", **kwargs)
        self.config["group_id"] = self.config.get("group_id", "sentinel.{}.canton".format(self.sentry_name))
        self.config["value_deserializer"] = json_deserializer

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        kwargs.update(settings.parameters)
        return cls(name=settings.name, **kwargs)

    async def on_message(self, message: ConsumerRecord) -> None:
        data = message.value
        try:
            update: CantonUpdate = self.record_type(**data)
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_update(update)

    async def on_update(self, update: CantonUpdate) -> None: ...
