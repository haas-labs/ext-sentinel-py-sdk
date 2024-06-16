from pydantic import BaseModel
from sentinel.db.monitoring_conditions.remote import RemoteMonitoringConditionsDB
from sentinel.models.database import Database


class ConditionsModel(BaseModel):
    threshold: int = 100


def test_remote_monitoring_conditions_db_init():
    conditions = RemoteMonitoringConditionsDB(
        name="TestMonitoringConditions",
        network="ethereum",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        bootstrap_servers="kafka-server",
        topics=["sentinel.monitoring-conditions.0123"],
        model="test_remote_monitoring_conditions.ConditionsModel",
        schema={"name": "conditions-schema", "version": "0.1.0"},
    )
    assert isinstance(conditions, RemoteMonitoringConditionsDB), "Incorrect Remote Monitoring Conditions DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"


def test_remote_monitoring_conditions_db_from_settings():
    conditions = RemoteMonitoringConditionsDB.from_settings(
        settings=Database(
            type="sentinel.db.monitoring_conditions.core.CoreMonitoringConditionsDB",
            parameters={
                "network": "ethereum",
                "bootstrap_servers": "kafka-server",
                "topics": ["sentinel.monitoring-conditions.0123"],
                "model": "test_remote_monitoring_conditions.ConditionsModel",
                "schema": {"name": "conditions-schema", "version": "0.1.0"},
            },
        ),
        sentry_name="Test-Sentry",
        sentry_hash="12345",
    )
    assert isinstance(conditions, RemoteMonitoringConditionsDB), "Incorrect Remote Monitoring Conditions DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"
