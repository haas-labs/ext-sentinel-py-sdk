from aiokafka.structs import ConsumerRecord
from aiokafka import AIOKafkaConsumer as KafkaConsumer

from sentinel.utils.logger import get_logger
from sentinel.channels.kafka.common import KafkaChannel


class InboundKafkaChannel(KafkaChannel):
    name = "inbound_kafka_channel"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        super().__init__(name, record_type, **kwargs)
        self.logger = get_logger(__name__)

        # Setting default values for auto_offset_reset
        self.config["auto_offset_reset"] = self.config.get("auto_offset_reset", "latest")

    async def run(self):
        """
        Run Inbound Kafka Channel
        """
        group_id = self.config.get("group_id", "unspecified")
        self.logger.info(f"{self.name} -> Subscribing to Kafka topics: {self.topics}, group id: {group_id}")
        self.consumer = KafkaConsumer(*self.topics, **self.config)

        self.logger.info(f"{self.name} -> Starting consuming messages fromn Kafka channel: {self.name}")
        await self.consumer.start()
        try:
            async for msg in self.consumer:
                await self.on_message(msg)
        finally:
            await self.consumer.stop()

    async def on_message(self, message: ConsumerRecord) -> None: ...
