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


class ConsumerChannel(Channel):
    """
    Consumer Channel
    """

    async def on_message(self, message: Any) -> None:
        """
        Handle consumer message
        """
        pass


class ProducerChannel(Channel):
    """
    Producer Channel
    """

    async def send(self, message: Any) -> None:
        """
        Sending a message to a channel
        """
        pass
