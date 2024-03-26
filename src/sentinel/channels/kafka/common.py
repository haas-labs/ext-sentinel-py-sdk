from sentinel.utils.logger import get_logger
from sentinel.channels.common import Channel


class KafkaChannel(Channel):
    name = "kafka_channel"

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Kafka Channel Init
        """
        super().__init__(name=name, record_type=record_type, **kwargs)
        self.logger = get_logger(__name__)

        self.logger.info(f"{self.name} -> Connecting to Kafka: {kwargs}")

        # Topics
        self.topics = self.config.pop("topics")

        # Botstrap server(-s)
        bootstrap_servers = self.config.get("bootstrap_servers")
        if isinstance(bootstrap_servers, (list, tuple)):
            self.config["bootstrap_servers"] = ",".join(bootstrap_servers)
