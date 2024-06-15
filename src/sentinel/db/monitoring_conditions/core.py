from pydantic import BaseModel, create_model
from sentinel.models.database import Database
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger


class CoreMonitoringConditionsDB:
    name = "monitoring_conditions"

    def __init__(self, name: str, network: str, model: str = None) -> None:
        self.name = name if name else self.name
        self.network = network
        if model is not None or model != "":
            _, model = import_by_classpath(model)
        self.model: BaseModel = create_model(
            "MonitoringConditionsModel",
            monitored_address=(str, None),
            monitoring_id=(int, None),
            conditions=(BaseModel, None),
            __base__=model,
        )

        self.logger = get_logger(__name__)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        network = settings.parameters.pop("network")
        model = settings.parameters.pop("model")
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            network=network,
            model=model,
            **kwargs,
        )

    def update(self) -> None: ...
