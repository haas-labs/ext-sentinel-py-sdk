import asyncio

import aiokafka
from sentinel.db.config.core import CoreConfigDB


class RemoteConfigDB(CoreConfigDB):
    def update(self) -> None:
        consumer = aiokafka.AIOKafkaConsumer()
        asyncio
