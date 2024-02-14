import logging

from sentinel.utils import import_by_classpath


logger = logging.getLogger(__name__)


class KafkaChannel:
    """
    Kafka Channel
    """

    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        """
        Kafka Channel Init
        """
        self.name = name
        _, self.record_type = import_by_classpath(record_type)

        logger.info(f"{self.name} -> Connecting to Kafka: {kwargs}")

        self.config = kwargs.copy()

        # Topics
        self.topics = self.config.pop("topics")

        # Botstrap server(-s)
        bootstrap_servers = self.config.get("bootstrap_servers")
        if isinstance(bootstrap_servers, (list, tuple)):
            self.config["bootstrap_servers"] = ",".join(bootstrap_servers)
