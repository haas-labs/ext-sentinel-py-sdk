from pydantic import BaseModel
from sentinel.db.monitoring_conditions.core import CoreMonitoringConditionsDB
from sentinel.models.database import Database


class ConditionsModel(BaseModel):
    threshold: int = 100


def test_core_monitoring_conditions_db_init():
    conditions = CoreMonitoringConditionsDB(
        name="TestMonitoringConditions",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        network="ethereum",
        model="test_core_monitoring_conditions.ConditionsModel",
    )
    assert isinstance(conditions, CoreMonitoringConditionsDB), "Incorrect Core Monitoring Conditions DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"


def test_core_monitoring_conditions_db_from_settings():
    conditions = CoreMonitoringConditionsDB.from_settings(
        settings=Database(
            type="sentinel.db.monitoring_conditions.core.CoreMonitoringConditionsDB",
            parameters={"network": "ethereum", "model": "test_core_monitoring_conditions.ConditionsModel"},
        ),
        sentry_name="Test-Sentry",
        sentry_hash="12345",
    )
    assert isinstance(conditions, CoreMonitoringConditionsDB), "Incorrect Core Monitoring Conditions DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"
