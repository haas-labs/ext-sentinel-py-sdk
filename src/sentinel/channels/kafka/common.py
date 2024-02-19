import logging

from sentinel.channels.common import Channel

logger = logging.getLogger(__name__)


class KafkaChannel(Channel):
    """
    Kafka Channel
    """

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
