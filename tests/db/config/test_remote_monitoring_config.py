from typing import Dict, Optional

import pytest
from pydantic import BaseModel, Field

from sentinel.db.config.remote import RemoteMonitoringConfigDB
from sentinel.models.database import Database


class ConsumerRecord(BaseModel):
    key: int
    value: Optional[Dict] = Field(default_factory=dict)


class ConfigModel(BaseModel):
    threshold: int = 100


@pytest.fixture
def monitoring_config_db():
    return RemoteMonitoringConfigDB(
        name="TestMonitoringConfig",
        network="ethereum",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        bootstrap_servers="kafka-server",
        topics=["sentinel.monitoring-config.0123"],
        model="test_remote_monitoring_config.ConfigModel",
        schema={"name": "Basic", "version": "1"},
    )


@pytest.fixture
def kafka_consumer_record() -> Dict:
    return {
        "id": 1705,
        "createdAt": 1716215314873,
        "updatedAt": 1716215314873,
        "status": "ACTIVE",
        "contract": {
            "id": 1371,
            "createdAt": 1716215314839,
            "updatedAt": 1716215314839,
            "projectId": 503,
            "tenantId": 519,
            "chainUid": "ethereum",
            "proxyAddress": None,
            "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "eth",
        },
        "schema": {
            "id": 1,
            "createdAt": 1717751852969,
            "updatedAt": 1717751852969,
            "status": "ACTIVE",
            "name": "Basic",
            "version": "1",
            "schema": {},
        },
        "name": "Attack Detector",
        "source": "ATTACK_DETECTOR",
        "tags": ["SECURITY"],
        "config": {},
        "destinations": [],
        "actions": [],
    }


def test_remote_monitoring_config_db_init(monitoring_config_db):
    assert isinstance(monitoring_config_db, RemoteMonitoringConfigDB), "Incorrect Remote Monitoring Config DB instance"
    assert monitoring_config_db.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert monitoring_config_db.sentry_hash == "12345", "Incorrect sentry hash"
    assert monitoring_config_db.get_group_id().startswith("sentinel.Test-Sentry."), "Incorrrect group id prefix"


def test_remote_monitoring_config_db_from_settings():
    configs = RemoteMonitoringConfigDB.from_settings(
        settings=Database(
            type="sentinel.db.config.core.CoreMonitoringConfigDB",
            parameters={
                "network": "ethereum",
                "bootstrap_servers": "kafka-server",
                "topics": ["sentinel.monitoring-config.0123"],
                "model": "test_remote_monitoring_config.ConfigModel",
                "schema": {"name": "config-schema", "version": "0.1.0"},
            },
        ),
        sentry_name="Test-Sentry",
        sentry_hash="12345",
    )
    assert isinstance(configs, RemoteMonitoringConfigDB), "Incorrect Remote Monitoring Configs DB instance"
    assert configs.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert configs.sentry_hash == "12345", "Incorrect sentry hash"


def test_remote_monitoring_config_db_add_remove_operations(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    monitoring_config_db.update(ConsumerRecord(key=1705, value=kafka_consumer_record))
    assert monitoring_config_db.size == 1, "Incorrect number of records in db"
    monitoring_config_db.update(ConsumerRecord(key=1705, value=None))
    assert monitoring_config_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_config_db_filter_by_source(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_record.copy()
    record["source"] = "FORTA"
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_config_db_filter_by_schame_and_version(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_record.copy()
    record["schema"]["name"] = "Invalid-Schema"
    record["schema"]["version"] = "0.1.0"
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_config_db_filter_by_network(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_record.copy()
    record["contract"]["chainUid"] = "bsc"
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_config_db_disabled_records(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_record.copy()
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 1, "Incorrect number of records in db"

    record = kafka_consumer_record.copy()
    record["status"] = "DISABLED"
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_config_db_duplicated_records(monitoring_config_db, kafka_consumer_record):
    assert len(monitoring_config_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_record.copy()
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 1, "Incorrect number of records in db"

    record = kafka_consumer_record.copy()
    monitoring_config_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_config_db.size == 1, "Incorrect number of records in db"
    assert monitoring_config_db.addresses == {
        "0xdac17f958d2ee523a2206206994597c13d831ec7": [1705]
    }, "Incorrect monitored addresses list"
