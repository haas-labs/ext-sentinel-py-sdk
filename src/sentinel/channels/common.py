from typing import Any
from sentinel.utils import import_by_classpath


class Channel:
    """
    Channel
    """

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Channel Init
        """
        self.name = name
        _, self.record_type = import_by_classpath(record_type)
        self.config = kwargs.copy()

    async def run(self):
        """
        Run Channel processing
        """
        raise NotImplementedError()


class InboundChannel(Channel):
    """
    Inbound Channel
    """

    async def on_message(self, message: Any) -> None:
        """
        Handle inbound message
        """
        pass


class OutboundChannel(Channel):
    """
    Outbound Channel
    """

    async def send(self, message: Any) -> None:
        """
        Sending a message to a channel
        """
        pass
