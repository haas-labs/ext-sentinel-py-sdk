from pydantic import BaseModel, create_model
from sentinel.models.database import Database
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger


class CoreMonitoringConditionsDB:
    name = "monitoring_conditions"

    def __init__(self, name: str, sentry_name: str, sentry_hash: str, network: str, model: str = None) -> None:
        self.name = name if name else self.name
        self.sentry_name = sentry_name
        self.sentry_hash = sentry_hash
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
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        network = settings.parameters.pop("network")
        model = settings.parameters.pop("model")
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            network=network,
            model=model,
            **kwargs,
        )

    def update(self) -> None: ...
