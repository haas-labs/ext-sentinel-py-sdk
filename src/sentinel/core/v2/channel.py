from typing import Any, List

from sentinel.core.v2.handler import FlowType, Handler
from sentinel.core.v2.instance import load_instance
from sentinel.models.channel import Channel as ChannelModel
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger


class Channel(Handler):
    def __init__(self, id: str, flow_type: FlowType, name: str, record_type: str, **kwargs) -> None:
        super().__init__(id=id, flow_type=flow_type, name=name, **kwargs)
        _, self.record_type = import_by_classpath(record_type)


class InboundChannel(Channel):
    name = "inbound_channel"

    # Handle inbound message
    async def on_message(self, message: Any) -> None: ...


class OutboundChannel(Channel):
    name = "outbound_channel"

    # Sending a message to a channel
    async def send(self, message: Any) -> None: ...


class Channels:
    def __init__(self, channels: List[ChannelModel]) -> None:
        self.logger = get_logger(__name__)

        for channel in channels:
            try:
                self.logger.info(f"Initializing channel: {channel.id}, type: {channel.type}")
                channel_instance: Channel = load_instance(id=channel.id, settings=channels)
                setattr(self, channel_instance.name, channel_instance)
            except (ValueError, AttributeError) as err:
                error_details = {
                    "id": channel.id,
                    "settings": channel.model_dump_json(),
                    "error": err,
                }
                self.logger.error(f"Channel initialization issue, {error_details}")
