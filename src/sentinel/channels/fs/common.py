import os
import json
import time
import asyncio
import pathlib
import aiofiles

from typing import Any, Dict

from sentinel.channels.common import InboundChannel, OutboundChannel


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class InboundFileChannel(InboundChannel):
    name = "inbound_file_channel"

    def __init__(
        self,
        name: str,
        record_type: str,
        path: pathlib.Path,
        time_interval: int = 0,
        **kwargs,
    ) -> None:
        """
        @param time_interval: int - the time interface between
                                    messages in seconfs, default: 0
        """
        super().__init__(name, record_type, **kwargs)
        self.path = path
        self.time_interval = time_interval

    async def run(self):
        """
        Run Channel Processing
        """
        async with aiofiles.open(self.path, mode="r") as source:
            async for raw_record in source:
                json_record = json.loads(raw_record)
                record = self.record_type(**json_record)
                await self.on_message(record)

                # Activate the time interface between messages in seconfs
                # WARNING! Blocking operation
                if self.time_interval > 0:
                    time.sleep(self.time_interval)

    async def on_message(self, message: Any) -> None: ...


class OutboundFileChannel(OutboundChannel):
    name = "outbound_file_channel"

    def __init__(
        self,
        name: str,
        record_type: str,
        path: pathlib.Path,
        mode: str = "append",
        buffering: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(name, record_type, **kwargs)

        self.buffering = buffering
        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)
        self.path = pathlib.Path(path) if isinstance(path, str) else path
        os.makedirs(self.path.parent, exist_ok=True)
        self.filemode = "a" if mode == "append" else "w"

    async def run(self):
        """
        Run Channel Processing
        """
        buffering = -1 if self.buffering else 1
        self.logger.info(
            f"{self.name} -> Starting channel for publishing messages to file channel: {self.name}, "
            + f"buffering: {self.buffering}"
        )
        async with aiofiles.open(self.path, mode=self.filemode, buffering=buffering) as target:
            while True:
                msg = await self.msg_queue.get()
                msg = json.dumps(msg)
                await target.write(f"{msg}\n")

    async def send(self, msg: Any) -> None:
        """
        Send message to in-process Queue
        """
        if isinstance(msg, Dict):
            msg = self.record_type(**msg)

        if isinstance(msg, self.record_type):
            await self.msg_queue.put(msg.model_dump(exclude_none=True))
        else:
            raise RuntimeError(f"Unknown message type, type: {type(msg)}, " + "supported: Dict or pydantic.BaseModel")
