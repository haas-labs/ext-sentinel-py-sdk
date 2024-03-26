from typing import Any

from sentinel.utils.logger import get_logger
from sentinel.utils.imports import import_by_classpath


class Channel:
    name: str = "unspecified"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Channel Init
        """
        self.name = name
        _, self.record_type = import_by_classpath(record_type)
        self.config = kwargs.copy()
        self.logger = get_logger(__name__)

    async def run(self) -> None:
        """
        Run Channel processing
        """
        raise NotImplementedError()


class InboundChannel(Channel):
    name = "inbound_channel"

    # Handle inbound message
    async def on_message(self, message: Any) -> None: ...


class OutboundChannel(Channel):
    name = "outbound_channel"

    # Sending a message to a channel
    async def send(self, message: Any) -> None: ...
