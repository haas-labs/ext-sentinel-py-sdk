import asyncio
import hashlib
import time
from collections import defaultdict
from typing import Dict, List

import aiokafka
from pydantic import BaseModel
from sentinel.channels.kafka.common import bytes2int_deserializer, json_deserializer
from sentinel.db.monitored_address.core import CoreMonitoredAddressDB
from sentinel.models.config import Configuration, Status

INGEST_TIMEOUT_SECS = 1
INGEST_TIMEOUT_MSECS = 1000


class SchemaVersion(BaseModel):
    name: str
    version: str


class RemoteMonitoredAddressDB(CoreMonitoredAddressDB):
    name = "config"

    def __init__(
        self,
        name: str,
        network: str,
        schema: SchemaVersion,
        bootstrap_servers: str,
        topics: List[str],
        model: BaseModel = None,
    ) -> None:
        super().__init__(name=name, network=network, model=model)

        self.schema = SchemaVersion(**schema)

        # Configuration Database
        self._config_db: Dict[int, Configuration] = {}

        # Monitored Address Database
        # The structure: <address> -> <config_id> -> <config itself>
        self._address_db: Dict[str, Dict] = defaultdict()

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

        self.logger.info(self.kafka_config)

    @property
    def addresses(self) -> Dict[str, Dict[int, Configuration]]:
        return dict(self._address_db)

    def get_group_id(self) -> str:
        channel_hash = hashlib.sha256(str(id(self)).encode("utf-8")).hexdigest()[:6]
        return f"sentinel.{self.name}-{channel_hash}.tx"

    def get_address(self, config: Configuration) -> str:
        return config.contract.proxy_address if config.contract.proxy_address is not None else config.contract.address

    def update(self, record: aiokafka.ConsumerRecord) -> None:
        if record.value is not None:
            config = Configuration(**record.value)

            """
            filtering schema by
            - ignore if source != ATTACK_DETECTOR
            - ignore if schema name and version is not matched with specified
            - ignore if network is not matched with specified
            - ignore if status != ACTIVE
            """

            # ATTACK_DETECTOR configs only
            if config.source != "ATTACK_DETECTOR":
                return

            # select configurations with specific schema and version only
            if config.config_schema.name != self.schema.name or config.config_schema.version != self.schema.version:
                return

            # handle configuration for predefined network only
            if config.contract.chain_uid != self.network:
                return

            # skip inactive config with removing active ones if present
            if config.status != Status.ACTIVE:
                if record.key in self._config_db:
                    config: Configuration = self._config_db.pop(record.key, None)
                    address = self.get_address(config=config)
                    if address is not None:
                        self._address_db[address].pop(config.id, None)
                        if len(self._address_db[address]) == 0:
                            del self._address_db[address]
                return

            self._config_db[record.key] = config
            address = self.get_address(config=config)
            if address not in self._address_db:
                self._address_db[address] = dict()
            self._address_db[address][config.id] = config.config

        else:
            self._config_db.pop(record.key, None)

    def ingest(self) -> None:
        async def ingest_records():
            consumer = aiokafka.AIOKafkaConsumer(*self.topics, **self.kafka_config)

            self.logger.info(f"{self.name} -> Starting consuming messages from Kafka channel: {self.name}")
            await consumer.start()
            try:
                last_msg_time = time.time()
                while True:
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
        self.logger.info(f"Monitored addresses detected: {len(self._address_db)}")
