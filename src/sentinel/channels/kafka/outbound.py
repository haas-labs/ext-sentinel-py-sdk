import json
import asyncio

from typing import Union, Dict

from pydantic import BaseModel

from aiokafka import AIOKafkaProducer as KafkaProducer

from sentinel.utils.logger import get_logger
from sentinel.channels.kafka.common import KafkaChannel


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000


class OutboundKafkaChannel(KafkaChannel):
    name = "outbound_kafka_channel"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        super().__init__(name, record_type, **kwargs)
        self.logger = get_logger(__name__)
        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)

    async def run(self):
        """
        Run Outbound Kafka Channel
        """
        self.logger.info(f"{self.name} -> Subscribing to Kafka topics: {self.topics}")
        self.producer = KafkaProducer(**self.config)

        self.logger.info(f"{self.name} -> Starting channel for publishing messages towards Kafka channel: {self.name}")
        await self.producer.start()
        try:
            while True:
                msg = await self.msg_queue.get()
                msg = bytes(json.dumps(msg), encoding="utf-8")
                for topic in self.topics:
                    await self.producer.send(topic=topic, value=msg)
        finally:
            await self.producer.stop()

    async def send(self, msg: Union[Dict, BaseModel]) -> None:
        """
        Send message to Producer Queue
        """
        if isinstance(msg, Dict):
            msg = self.record_type(**msg)

        if isinstance(msg, self.record_type):
            await self.msg_queue.put(msg.model_dump(exclude_none=True))
        else:
            raise RuntimeError(f"Unknown message type, type: {type(msg)}, " + "supported: Dict or pydantic.BaseModel")
