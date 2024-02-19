import json
import logging
import websockets

from typing import Any, Dict

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

        # Web socket server
        self.ws_server = self.config.get("server")


class InboundWebsocketChannel(WebsocketChannel):
    """
    Inbound Websocket Channel
    """
    async def run(self):
        """
        Run Inbound Websocket Channel Processing
        """
        logger.info(f"{self.name} -> Starting channel for consuming messages from websocket channel: {self.name}")

        try:
            async for msg in websockets.connect(self.ws_server):
                json_record = json.loads(msg)
                record = self._record_type(**json_record)
                await self.on_message(record)
        finally:
            logger.info(f"Closing connection to websocket channel: {self.name}")

    async def on_message(self, message: Any) -> None:
        pass
