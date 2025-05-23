import asyncio
import time
from typing import Dict, Iterator, List

import aiokafka
from pydantic import BaseModel

from sentinel.channels.kafka.common import bytes2int_deserializer, json_deserializer
from sentinel.db.monitoring_conditions.core import CoreMonitoringConditionsDB
from sentinel.models.config import Configuration, Status
from sentinel.utils.version import IncorrectVersionFormat, is_bugfix

INGEST_TIMEOUT_SECS = 5
INGEST_TIMEOUT_MSECS = INGEST_TIMEOUT_SECS * 1000

ATTACK_DETECTOR_SOURCE = "ATTACK_DETECTOR"


class SchemaVersion(BaseModel):
    name: str
    version: str


class RemoteMonitoringConditionsDB(CoreMonitoringConditionsDB):
    name = "monitoring_conditions"

    def __init__(
        self,
        name: str,
        network: str,
        sentry_name: str,
        sentry_hash: str,
        bootstrap_servers: str,
        topics: List[str],
        schema: Dict[str, str],
        model: BaseModel = None,
        **kwargs,
    ) -> None:
        super().__init__(name=name, sentry_name=sentry_name, sentry_hash=sentry_hash, network=network, model=model)

        self.schema = SchemaVersion(**schema)

        self.topics = topics

        self.kafka_config = {}
        # Bootstrap servers
        self.kafka_config["bootstrap_servers"] = bootstrap_servers
        # Setting default values for auto_offset_reset
        self.kafka_config["auto_offset_reset"] = "earliest"

        self.kafka_config["group_id"] = self.get_group_id()
        self.kafka_config["key_deserializer"] = bytes2int_deserializer
        self.kafka_config["value_deserializer"] = json_deserializer
        self.kafka_config["auto_offset_reset"] = "earliest"

        # Configuration Database
        # The structure: <config_id> -> <Configuration>
        self._config_db: Dict[int, Configuration] = {}

        # Monitored Address Database
        # The structure: <address> -> List[<config_id>]
        self._address_db: Dict[str, List[int]] = {}

    @property
    def addresses(self) -> Dict[str, Dict[int, Configuration]]:
        """
        returns the list addresses with monitoring conditions
        """
        return dict(self._address_db)

    def get_address_conditions(self, address: str) -> Iterator[Configuration]:
        """
        returns monitoring conditions for specific address
        """
        if address in self._address_db:
            for config_id in self._address_db[address]:
                yield self._config_db[config_id]

    def get_group_id(self) -> str:
        """
        returns Kafka group id
        """
        return f"sentinel.{self.sentry_name}.{self.sentry_hash}"

    def get_address(self, config: Configuration) -> str:
        """
        returns address or proxy
        """
        return config.contract.address

    def update(self, record: aiokafka.ConsumerRecord) -> None:
        # Skip empty/deleted record. Specific use case for Kafka implementation
        if record.value is None:
            return

        config = Configuration(**record.value)

        """
        filtering schema by
        - ignore if source != ATTACK_DETECTOR
        - ignore if schema name and version is not matched with specified
        - ignore if network is not matched with specified
        - ignore if status != ACTIVE
        """
        # Select ATTACK_DETECTOR configs only
        if config.source != ATTACK_DETECTOR_SOURCE:
            return

        # handle configuration for predefined network only
        if config.contract.chain_uid != self.network:
            return

        # select configurations with specific schema and version only
        try:
            if not (
                config.config_schema.name == self.schema.name
                and is_bugfix(
                    main_version=self.schema.version,
                    version=config.config_schema.version,
                )
            ):
                return
        except IncorrectVersionFormat as err:
            self.logger.error(f"Incorrect version format: {config}, error: {err}")
            return

        # Remove inactive (DISABLED, DELETED) configs from local databases: configs and addresses
        monitored_address = self.get_address(config=config)
        if config.status != Status.ACTIVE:
            if config.id in self._config_db:
                # Cleanup config database
                del self._config_db[config.id]
                # Cleanup address database
                if monitored_address is not None:
                    self._address_db[monitored_address].remove(config.id)
                    if len(self._address_db[monitored_address]) == 0:
                        del self._address_db[monitored_address]
            return

        # Proceed with active configs only
        self._config_db[config.id] = config
        if monitored_address not in self._address_db:
            self._address_db[monitored_address] = list()

        if config.id not in self._address_db[monitored_address]:
            self._address_db[monitored_address].append(config.id)

    def ingest(self) -> None:
        async def ingest_records():
            consumer = aiokafka.AIOKafkaConsumer(*self.topics, **self.kafka_config)

            self.logger.info(f"{self.name} -> Starting consuming messages from Kafka channel: {self.name}")
            await consumer.start()
            try:
                while True:
                    last_msg_time = time.time()
                    data = await consumer.getmany(timeout_ms=INGEST_TIMEOUT_MSECS)
                    if data:
                        for _, records in data.items():
                            for record in records:
                                self.update(record=record)
                    else:
                        if time.time() - last_msg_time > INGEST_TIMEOUT_SECS:
                            self.logger.info(
                                f"No new messages received in the last {INGEST_TIMEOUT_SECS} seconds. Stopping ingest"
                            )
                            break
            finally:
                await consumer.stop()

        asyncio.run(ingest_records())
        self.logger.info(f"Monitored addresses detected: {self.size}")
