from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field
from sentinel.core.v2.handler import FlowType, Handler
from sentinel.core.v2.instance import load_instance
from sentinel.models.channel import Channel as ChannelModel
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import Logger


class Channel(BaseModel):
    type: str
    name: Optional[str] = None
    id: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[Dict] = Field(default_factory=dict)
    flow_type: FlowType = None
    instance: Optional[Any] = None
    label: Optional[Dict[str, str]] = Field(default_factory=dict)


class ChannelHandler(Handler):
    name = "channel_handler"

    def __init__(self, id: str, flow_type: FlowType, record_type: str, name: str = None, **kwargs) -> None:
        super().__init__(id=id, flow_type=flow_type, name=name, **kwargs)
        _, self.record_type = import_by_classpath(record_type)


class InboundChannel(ChannelHandler):
    name = "inbound_channel"

    def __init__(self, id: str, record_type: str, name: str = None, **kwargs) -> None:
        super().__init__(id=id, flow_type=FlowType.inbound, record_type=record_type, name=name, **kwargs)

    # Handle inbound message
    async def on_message(self, message: Any) -> None: ...


class OutboundChannel(ChannelHandler):
    name = "outbound_channel"

    def __init__(self, id: str, record_type: str, name: str = None, **kwargs) -> None:
        super().__init__(id=id, flow_type=FlowType.outbound, record_type=record_type, name=name, **kwargs)

    # Sending a message to a channel
    async def send(self, message: Any) -> None: ...


class Channels:
    def __init__(self, channels: List[ChannelModel], logger: Logger, **kwargs) -> None:
        self.logger = logger
        self.names = list()
        self.kwargs = kwargs

        self.init(channels=channels)

    def init(self, channels: List[Channel]) -> None:
        for channel in channels:
            try:
                self.logger.info(f"Initializing channel: {channel.id}, type: {channel.type}, kwargs: {self.kwargs}")
                channel_instance: ChannelHandler = load_instance(settings=channel, **self.kwargs)
                setattr(self, channel_instance.name, channel_instance)
                self.names.append(channel_instance.name)
            except (ValueError, AttributeError) as err:
                error_details = {
                    "id": channel.id,
                    "settings": channel.model_dump_json(),
                    "error": err,
                }
                self.logger.error(f"Channel initialization issue, {error_details}")

    def __iter__(self):
        for ch_name in self.names:
            yield getattr(self, ch_name)
