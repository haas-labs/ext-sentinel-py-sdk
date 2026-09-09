from typing import Dict, Optional

import pytest
from pydantic import BaseModel, Field

from sentinel.db.monitoring_conditions.remote import RemoteMonitoringConditionsDB
from sentinel.models.database import Database


class ConsumerRecord(BaseModel):
    key: int
    value: Optional[object] = Field(default_factory=dict)
    offset: int = 0


class ConditionsModel(BaseModel):
    threshold: int = 100


@pytest.fixture
def monitoring_conditions_db():
    return RemoteMonitoringConditionsDB(
        name="TestMonitoringConditions",
        network="ethereum",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        bootstrap_servers="kafka-server",
        topics=["sentinel.monitoring-conditions.0123"],
        model="test_remote_monitoring_conditions.ConditionsModel",
        schema={"name": "Basic", "version": "1.1.1"},
    )


@pytest.fixture
def kafka_consumer_active_record() -> Dict:
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
            "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "eth",
        },
        "schema": {
            "id": 1,
            "createdAt": 1717751852969,
            "updatedAt": 1717751852969,
            "status": "ACTIVE",
            "name": "Basic",
            "version": "1.1.1",
            "schema": {},
        },
        "name": "Attack Detector",
        "source": "ATTACK_DETECTOR",
        "tags": ["SECURITY"],
        "config": {},
        "destinations": [],
        "actions": [],
    }


@pytest.fixture
def kafka_consumer_disabled_record() -> Dict:
    return {
        "id": 1705,
        "createdAt": 1716215314873,
        "updatedAt": 1716215314873,
        "status": "DISABLED",
        "contract": {
            "id": 1371,
            "createdAt": 1716215314839,
            "updatedAt": 1716215314839,
            "projectId": 503,
            "tenantId": 519,
            "chainUid": "ethereum",
            "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "eth",
        },
        "schema": {
            "id": 1,
            "createdAt": 1717751852969,
            "updatedAt": 1717751852969,
            "status": "ACTIVE",
            "name": "Basic",
            "version": "1.1.1",
            "schema": {},
        },
        "name": "Attack Detector",
        "source": "ATTACK_DETECTOR",
        "tags": ["SECURITY"],
        "config": {},
        "destinations": [],
        "actions": [],
    }


@pytest.fixture
def kafka_consumer_deleted_record() -> Dict:
    return {
        "id": 1705,
        "createdAt": 1716215314873,
        "updatedAt": 1716215314873,
        "status": "DELETED",
        "contract": {
            "id": 1371,
            "createdAt": 1716215314839,
            "updatedAt": 1716215314839,
            "projectId": 503,
            "tenantId": 519,
            "chainUid": "ethereum",
            "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
            "name": "eth",
        },
        "schema": {
            "id": 1,
            "createdAt": 1717751852969,
            "updatedAt": 1717751852969,
            "status": "ACTIVE",
            "name": "Basic",
            "version": "1.1.1",
            "schema": {},
        },
        "name": "Attack Detector",
        "source": "ATTACK_DETECTOR",
        "tags": ["SECURITY"],
        "config": {},
        "destinations": [],
        "actions": [],
    }


def test_remote_monitoring_conditions_db_init(monitoring_conditions_db):
    assert isinstance(
        monitoring_conditions_db, RemoteMonitoringConditionsDB
    ), "Incorrect Remote Monitoring Conditions DB instance"
    assert monitoring_conditions_db.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert monitoring_conditions_db.sentry_hash == "12345", "Incorrect sentry hash"
    assert monitoring_conditions_db.get_group_id().startswith("sentinel.Test-Sentry."), "Incorrrect group id prefix"


def test_remote_monitoring_conditions_db_from_settings():
    conditions = RemoteMonitoringConditionsDB.from_settings(
        settings=Database(
            type="sentinel.db.monitoring_conditions.core.CoreMonitoringConditionsDB",
            parameters={
                "network": "ethereum",
                "bootstrap_servers": "kafka-server",
                "topics": ["sentinel.monitoring-conditions.0123"],
                "model": "test_remote_monitoring_conditions.ConditionsModel",
                "schema": {"name": "conditions-schema", "version": "0.1.1"},
            },
        ),
        sentry_name="Test-Sentry",
        sentry_hash="12345",
    )
    assert isinstance(conditions, RemoteMonitoringConditionsDB), "Incorrect Remote Monitoring Conditions DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"


def test_remote_monitoring_conditions_db_add_remove_operations(
    monitoring_conditions_db,
    kafka_consumer_active_record,
    kafka_consumer_disabled_record,
    kafka_consumer_deleted_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    # No reactions on null records
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_active_record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=None))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"

    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_active_record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_disabled_record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"

    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_active_record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_deleted_record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_filter_by_source(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_active_record.copy()
    record["source"] = "FORTA"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_filter_by_schame_and_version(
    monitoring_conditions_db, kafka_consumer_active_record
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_active_record.copy()
    record["schema"]["name"] = "Invalid-Schema"
    record["schema"]["version"] = "0.1.1"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_filter_by_network(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_active_record.copy()
    record["contract"]["chainUid"] = "bsc"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_disabled_records(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_active_record.copy()
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"

    record = kafka_consumer_active_record.copy()
    record["status"] = "DISABLED"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_duplicated_records(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    record = kafka_consumer_active_record.copy()
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"

    record = kafka_consumer_active_record.copy()
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"
    assert monitoring_conditions_db.addresses == {
        "0xdac17f958d2ee523a2206206994597c13d831ec7": [1705]
    }, "Incorrect monitored addresses list"


def test_remote_monitoring_conditions_db_ignores_another_source_the_model_cannot_parse(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    """
    The topic is shared. A record from another producer can carry values this model rejects —
    dev has WORKFLOW records with status UNKNOWN — and one of them used to raise out of update(),
    abort the whole ingest, and leave the sentry with no addresses at all.
    """
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    foreign = {"id": 1, "status": "UNKNOWN", "source": "WORKFLOW", "name": "ReportContext"}
    monitoring_conditions_db.update(ConsumerRecord(key=1, value=foreign, offset=6901))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"

    # and the records that follow it still land
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_active_record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"


def test_remote_monitoring_conditions_db_ignores_our_own_malformed_record(
    monitoring_conditions_db,
    kafka_consumer_active_record,
):
    assert len(monitoring_conditions_db.addresses) == 0, "Expect to have empty db"

    malformed = kafka_consumer_active_record.copy()
    malformed["status"] = "UNKNOWN"
    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=malformed, offset=42))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"

    monitoring_conditions_db.update(ConsumerRecord(key=1705, value=kafka_consumer_active_record))
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in db"


@pytest.mark.parametrize(
    "value",
    [
        {},
        {"source": "ATTACK_DETECTOR"},
        {"source": "ATTACK_DETECTOR", "id": "not-an-int"},
        {"source": "ATTACK_DETECTOR", "status": "UNKNOWN"},
        {"source": "ATTACK_DETECTOR", "contract": "not-an-object"},
        {"source": "WORKFLOW", "status": "UNKNOWN"},
        {"source": None},
        [],
        "a string",
        42,
    ],
)
def test_remote_monitoring_conditions_db_update_never_raises(monitoring_conditions_db, value):
    """
    A record is data, not a contract. update() is called per record both by the ingest rebuild
    and, live, by every detector's on_config_change — so no shape may raise out of it.
    """
    monitoring_conditions_db.update(ConsumerRecord(key=1, value=value, offset=1))
    assert monitoring_conditions_db.size == 0, "Incorrect number of records in db"

