import json
import time
import asyncio
import logging
import pathlib
import aiofiles

from typing import Any, Dict

from sentinel.channels.common import InboundChannel, OutboundChannel


logger = logging.getLogger(__name__)


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class InboundWebsocketChannel(InboundChannel):
    """
    Inbound Websocket Channel
    """

    def __init__(
        self,
        name: str,
        record_type: str,
        **kwargs,
    ) -> None:
        """
        Inbound Websocket Channel Init
        """
        super().__init__(name, record_type, **kwargs)

    async def run(self):
        """
        Run Inbound Websocket Channel Processing
        """

        raise NotImplementedError()

        # logger.info(f"{self.name} -> Starting channel for consuming messages from websocket channel: {self.name}")
        # async with aiofiles.open(self.path, mode="r") as source:
        #     async for raw_record in source:
        #         json_record = json.loads(raw_record)
        #         record = self.record_type(**json_record)
        #         await self.on_message(record)

    async def on_message(self, message: Any) -> None:
        pass


class OutboundWebsocketChannel(OutboundChannel):
    """
    Outbound Websocket Channel
    """

    def __init__(
        self,
        name: str,
        record_type: str,
        **kwargs,
    ) -> None:
        """
        Outbound Websocket Channel Init
        """
        super().__init__(name, record_type, **kwargs)
        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)

    async def run(self):
        """
        Run Inbound Websocket Channel Processing
        """
        raise NotImplementedError()

        # logger.info(f"{self.name} -> Starting channel for publishing messages to websocket channel: {self.name}")
        # async with aiofiles.open(self.path, mode=self.filemode) as target:
        #     while True:
        #         msg = await self.msg_queue.get()
        #         msg = json.dumps(msg)
        #         await target.write(f"{msg}\n")

    async def send(self, msg: Any) -> None:
        """
        Send message to in-process Queue
        """
        if isinstance(msg, Dict):
            msg = self.record_type(**msg)

        if isinstance(msg, self.record_type):
            self.msg_queue.put_nowait(msg.model_dump(exclude_none=True))
        else:
            raise RuntimeError(f"Unknown message type, type: {type(msg)}, " + "supported: Dict or pydantic.BaseModel")
