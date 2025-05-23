import json
from typing import Any, Optional

from sentinel.channels.common import Channel


def json_deserializer(serialized: Optional[str]) -> Optional[Any]:
    """
    JSON Deserializer
    """
    if serialized is None:
        return None
    try:
        return json.loads(serialized)
    except json.decoder.JSONDecodeError:
        return None


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
        self.logger.info(f"{self.name} -> Connecting to Kafka: {kwargs}")

        # Sentry Details
        kwargs = kwargs.copy()
        self.sentry_name = self.config.pop("sentry_name")
        self.sentry_hash = self.config.pop("sentry_hash")

        # Topics
        self.topics = self.config.pop("topics")

        # Botstrap server(-s)
        bootstrap_servers = self.config.get("bootstrap_servers")
        if isinstance(bootstrap_servers, (list, tuple)):
            self.config["bootstrap_servers"] = ",".join(bootstrap_servers)
