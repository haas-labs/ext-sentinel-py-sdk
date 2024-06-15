from pydantic import BaseModel
from sentinel.db.monitoring_conditions.core import CoreMonitoringConditionsDB
from sentinel.models.database import Database


class ConditionsModel(BaseModel):
    threshold: int = 100


def test_core_monitoring_conditions_db_init():
    conditions = CoreMonitoringConditionsDB(
        name="TestMonitoringConditions", network="ethereum", model="test_core_monitoring_conditions.ConditionsModel"
    )
    assert isinstance(conditions, CoreMonitoringConditionsDB), "Incorrect Core Monitoring Conditions DB instance"


def test_core_monitoring_conditions_db_from_settings():
    conditions = CoreMonitoringConditionsDB.from_settings(
        settings=Database(
            type="sentinel.db.monitoring_conditions.core.CoreMonitoringConditionsDB",
            parameters={"network": "ethereum", "model": "test_core_monitoring_conditions.ConditionsModel"},
        )
    )
    assert isinstance(conditions, CoreMonitoringConditionsDB), "Incorrect Core Monitoring Conditions DB instance"
