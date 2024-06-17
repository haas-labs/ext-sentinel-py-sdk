import pytest
from pydantic import BaseModel
from sentinel.db.monitoring_conditions.core import Conditions, CoreMonitoringConditionsDB
from sentinel.models.database import Database


@pytest.fixture
def monitoring_conditions_db():
    return CoreMonitoringConditionsDB(
        name="TestMonitoringConditions",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        network="ethereum",
        model="test_core_monitoring_conditions.ConditionsModel",
    )


class ConditionsModel(BaseModel):
    threshold: int = 100


def test_core_monitoring_conditions_db_init(monitoring_conditions_db):
    assert isinstance(
        monitoring_conditions_db, CoreMonitoringConditionsDB
    ), "Incorrect Core Monitoring Conditions DB instance"
    assert monitoring_conditions_db.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert monitoring_conditions_db.sentry_hash == "12345", "Incorrect sentry hash"


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


def test_core_monitoring_conditions_db_operations(monitoring_conditions_db):
    condition_a = Conditions(address="0x12345", conditions={"threshold": 100})
    monitoring_conditions_db.update(condition_a)
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in monitoring conditions db"
    assert monitoring_conditions_db.has_address(condition_a.address), "Missed address in monitoring conditions db"

    condition_b = Conditions(address="0x12345", conditions={"threshold": 150})
    monitoring_conditions_db.update(condition_b)
    assert monitoring_conditions_db.size == 1, "Incorrect number of records in monitoring conditions db"
