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
            async for ws_server in websockets.connect(self.server_uri):
                logger.info(f"Connecting to websocket, {self.server_uri}")
                try:
                    async for msg in ws_server:
                        json_record = json.loads(msg)
                        record = self.record_type(**json_record)
                        await self.on_message(record)
                except websockets.ConnectionClosed as err:
                    logger.warning(f"Connection to websocket closed, {err}")
                    continue
        finally:
            logger.info(f"Closing connection to websocket channel: {self.name}")

    async def on_message(self, message: Any) -> None:
        pass
