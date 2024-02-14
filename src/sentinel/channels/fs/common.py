import json
import time
import asyncio
import logging
import pathlib
import aiofiles

from typing import Any, Dict

from sentinel.channels.common import ConsumerChannel, ProducerChannel

from sentinel.models.event import Event


logger = logging.getLogger(__name__)


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class ConsumerFileChannel(ConsumerChannel):
    """
    Consumer File Channel
    """

    def __init__(
        self,
        name: str,
        record_type: str,
        path: pathlib.Path,
        time_interval: int = 0,
        **kwargs,
    ) -> None:
        """
        Consumer File Channel Init

        @param time_interval: int - the time interface between
                                    messages in seconfs, default: 0
        """
        super().__init__(name, record_type, **kwargs)
        self.path = path
        self.time_interval = time_interval

    async def run(self):
        """
        Run Consumer File Channel Processing
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

    async def on_message(self, message: Any) -> None:
        pass


class ProducerFileChannel(ProducerChannel):
    """
    Producer File Channel
    """

    def __init__(
        self,
        name: str,
        record_type: str,
        path: pathlib.Path,
        mode: str = "append",
        **kwargs,
    ) -> None:
        """
        Producer File Channel Init
        """
        super().__init__(name, record_type, **kwargs)

        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)
        self.path = path
        self.filemode = "a" if mode == "append" else "w"

    async def run(self):
        """
        Run Producer File Channel Processing
        """
        logger.info(
            f"{self.name} -> Starting channel for publishing messages to file channel: {self.name}"
        )
        async with aiofiles.open(self.path, mode=self.filemode) as target:
            while True:
                msg = await self.msg_queue.get()
                msg = json.dumps(msg)
                await target.write(f"{msg}\n")

    async def send(self, msg: Any) -> None:
        """
        Send message to Producer Queue
        """
        if isinstance(msg, Dict):
            msg = self.record_type(**msg)

        if isinstance(msg, self.record_type):
            self.msg_queue.put_nowait(msg.model_dump(exclude_none=True))
        else:
            raise RuntimeError(
                f"Unknown message type, type: {type(msg)}, "
                + "supported: Dict or pydantic.BaseModel"
            )
