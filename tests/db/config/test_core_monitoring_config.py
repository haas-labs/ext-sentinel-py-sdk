import pytest
from pydantic import BaseModel

from sentinel.db.config.core import Config, CoreMonitoringConfigDB
from sentinel.models.database import Database


@pytest.fixture
def monitoring_config_db():
    return CoreMonitoringConfigDB(
        name="TestMonitoringConfig",
        sentry_name="Test-Sentry",
        sentry_hash="12345",
        network="ethereum",
        model="test_core_monitoring_config.ConfigModel",
    )


class ConfigModel(BaseModel):
    threshold: int = 100


def test_core_monitoring_config_db_init(monitoring_config_db):
    assert isinstance(monitoring_config_db, CoreMonitoringConfigDB), "Incorrect Core Monitoring Config DB instance"

    assert monitoring_config_db.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert monitoring_config_db.sentry_hash == "12345", "Incorrect sentry hash"


def test_core_monitoring_config_db_from_settings():
    conditions = CoreMonitoringConfigDB.from_settings(
        settings=Database(
            type="sentinel.db.config.core.CoreMonitoringConfigDB",
            parameters={"network": "ethereum", "model": "test_core_monitoring_config.ConfigModel"},
        ),
        sentry_name="Test-Sentry",
        sentry_hash="12345",
    )
    assert isinstance(conditions, CoreMonitoringConfigDB), "Incorrect Core Monitoring Config DB instance"
    assert conditions.sentry_name == "Test-Sentry", "Incorrect sentry hash"
    assert conditions.sentry_hash == "12345", "Incorrect sentry hash"


def test_core_monitoring_config_db_operations(monitoring_config_db):
    config_a = Config(address="0x12345", parameters={"threshold": 100})
    monitoring_config_db.update(config_a)
    assert monitoring_config_db.size == 1, "Incorrect number of records in monitoring config db"
    assert monitoring_config_db.has_address(config_a.address), "Missed address in monitoring config db"

    config_b = Config(address="0x12345", conditions={"threshold": 150})
    monitoring_config_db.update(config_b)
    assert monitoring_config_db.size == 1, "Incorrect number of records in monitoring config db"
