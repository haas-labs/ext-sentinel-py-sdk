import json

from sentinel.channels.common import Channel
from sentinel.utils.logger import logger


def json_deserializer(serialized):
    """
    JSON Deserializer
    """
    if serialized is None:
        return None
    return json.loads(serialized)


def bytes2int_deserializer(serialized: bytes) -> int:
    if serialized is None:
        return None
    return int.from_bytes(serialized, byteorder="big")


class KafkaChannel(Channel):
    name = "kafka_channel"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Kafka Channel Init
        """
        super().__init__(name=name, record_type=record_type, **kwargs)

        logger.info(f"{self.name} -> Connecting to Kafka: {kwargs}")

        # Topics
        self.topics = self.config.pop("topics")

        # Botstrap server(-s)
        bootstrap_servers = self.config.get("bootstrap_servers")
        if isinstance(bootstrap_servers, (list, tuple)):
            self.config["bootstrap_servers"] = ",".join(bootstrap_servers)
