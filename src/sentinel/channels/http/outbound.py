import logging

from typing import Dict

from sentinel.models.event import Event
from sentinel.channels.http.common import OutboundHTTPChannel

logger = logging.getLogger(__name__)


class OutboundEventsChannel(OutboundHTTPChannel):
    name = "events"
    
    def __init__(self, name: str, metadata: Dict = dict(), **kwargs) -> None:
        """
        Event Kafka Channel
        """
        super().__init__(name, record_type="sentinel.models.event.Event", **kwargs)
        self._default_metadata = metadata.copy()

    async def send(self, msg: Event) -> None:
        """
        Send Event via HTTP/REST interface
        """
        # Add default metadata fields only if there are no such fields
        for k, v in self._default_metadata.items():
            if k not in msg.metadata:
                msg.metadata[k] = v

        if not isinstance(msg, Event):
            logger.error(f"Incorrect message type, expected: Event, detected: {type(msg)}")

        await super().send(msg)

