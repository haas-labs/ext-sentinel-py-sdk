import json
import websockets

from typing import Any

from sentinel.channels.common import Channel


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class WebsocketChannel(Channel):
    name = "websocket_channel"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        super().__init__(name=name, record_type=record_type, **kwargs)

        # Web socket server URI
        self.server_uri = self.config.get("server_uri")


class InboundWebsocketChannel(WebsocketChannel):
    name = "inbound_websocket_channel"

    async def run(self):
        """
        Run Inbound Websocket Channel Processing
        """
        try:
            async for ws_server in websockets.connect(self.server_uri):
                self.logger.info(f"Connecting to websocket, {self.server_uri}")
                try:
                    async for msg in ws_server:
                        json_record = json.loads(msg)
                        record = self.record_type(**json_record)
                        await self.on_message(record)
                except websockets.ConnectionClosed as err:
                    self.logger.warning(f"Connection to websocket closed, {err}")
                    continue
        finally:
            self.logger.info(f"Closing connection to websocket channel: {self.name}")

    async def on_message(self, message: Any) -> None: ...
