import asyncio
import json
import os
import pathlib
import time
from typing import Any, Dict

import aiofiles
from sentinel.channels.common import InboundChannel, OutboundChannel
from sentinel.core.v2.channel import Channel
from sentinel.utils.logger import get_logger

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
        super().__init__(name=name, record_type=record_type, **kwargs)

        if path is None or path == "":
            raise ValueError(f"The 'path' parameter is missing or specified incorrectly, path: {path}")
        self.path = path
        self.time_interval = time_interval

    @classmethod
    def from_settings(cls, settings: Channel):
        parameters = settings.parameters.copy()
        return cls(
            name=settings.name,
            record_type=parameters.get("record_type"),
            path=pathlib.Path(parameters.get("path")),
            time_interval=parameters.get("time_interval", 0),
        )

    async def run(self):
        """
        Run Channel Processing
        """
        self.logger = get_logger(__name__)
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
        stop_after: int = 0,
        **kwargs,
    ) -> None:
        super().__init__(name=name, record_type=record_type, **kwargs)

        self.buffering = buffering
        if path is None or path == "":
            raise ValueError(f"The 'path' parameter is missing or specified incorrectly, path: {path}")
        self.path = pathlib.Path(path) if isinstance(path, str) else path
        self.filemode = "a" if mode == "append" else "w"
        os.makedirs(self.path.parent, exist_ok=True)

        # Stop processing after N records
        self.stop_after = stop_after

        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        parameters = settings.parameters.copy()
        return cls(
            name=settings.name,
            record_type=parameters.get("record_type"),
            path=pathlib.Path(parameters.get("path")),
            mode=parameters.get("mode", "append"),
            buffering=parameters.get("buffering", False),
            stop_after=parameters.get("stop_after", 0),
            **kwargs,
        )

    async def run(self):
        """
        Run Channel Processing
        """
        self.logger = get_logger(__name__)

        buffering = -1 if self.buffering else 1
        self.logger.info(
            f"{self.name} -> Starting channel for publishing messages to file channel: {self.name}, "
            + f"buffering: {self.buffering}"
        )
        total_records = 0
        async with aiofiles.open(self.path, mode=self.filemode, buffering=buffering) as target:
            while True:
                total_records += 1
                msg = await self.msg_queue.get()
                msg = json.dumps(msg)
                await target.write(f"{msg}\n")
                if self.stop_after > 0 and total_records >= self.stop_after:
                    break

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
