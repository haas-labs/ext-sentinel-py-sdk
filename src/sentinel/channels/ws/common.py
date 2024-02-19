import json
import logging
import websockets

from typing import Any

from sentinel.channels.common import Channel


logger = logging.getLogger(__name__)


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class WebsocketChannel(Channel):
    """
    Websocket Channel
    """

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Kafka Channel Init
        """
        super().__init__(name=name, record_type=record_type, **kwargs)

        logger.info(f"{self.name} -> Connecting to Websocket server: {kwargs}")

        # Web socket server URI
        self.server_uri = self.config.get("server_uri")


class InboundWebsocketChannel(WebsocketChannel):
    """
    Inbound Websocket Channel
    """
    async def run(self):
        """
        Run Inbound Websocket Channel Processing
        """
        try:
            async with websockets.connect(self.server_uri) as ws_server:
                async for msg in ws_server:
                    json_record = json.loads(msg)
                    record = self.record_type(**json_record)
                    await self.on_message(record)
        finally:
            logger.info(f"Closing connection to websocket channel: {self.name}")

    async def on_message(self, message: Any) -> None:
        pass
