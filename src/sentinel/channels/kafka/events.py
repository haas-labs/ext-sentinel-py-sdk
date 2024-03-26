from typing import Dict


from aiokafka.structs import ConsumerRecord

from sentinel.models.event import Event

from sentinel.utils.logger import get_logger
from sentinel.transform import json_deserializer
from sentinel.channels.kafka.inbound import InboundKafkaChannel
from sentinel.channels.kafka.outbound import OutboundKafkaChannel


class InboundEventsChannel(InboundKafkaChannel):
    name = "events"

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(name, record_type="sentinel.models.event.Event", **kwargs)
        self.logger = get_logger(__name__)

        self.config["value_deserializer"] = json_deserializer

    async def on_message(self, message: ConsumerRecord) -> None:
        """
        Handle consumer message for events channel
        """
        data = message.value
        if data is None:
            return None
        try:
            event: Event = self.record_type(**data)
        except Exception as err:
            raise RuntimeError(f"Error: {err}, data: {data}")
        await self.on_event(event)

        # TODO add handling of events batch

    async def on_event(self, event: Event) -> None: ...


class OutboundEventsChannel(OutboundKafkaChannel):
    name = "events"

    def __init__(self, name: str, metadata: Dict = dict(), **kwargs) -> None:
        super().__init__(name, record_type="sentinel.models.event.Event", **kwargs)
        self.logger = get_logger(__name__)

        self._default_metadata = metadata.copy()

    async def send(self, msg: Event) -> None:
        """
        Send event via events
        """
        # Add default metadata fields only if there are no such fields
        for k, v in self._default_metadata.items():
            if k not in msg.metadata:
                msg.metadata[k] = v

        if not isinstance(msg, Event):
            raise RuntimeError(f"Incorrect message type, expected: Event, detected: {type(msg)}")

        await super().send(msg)
