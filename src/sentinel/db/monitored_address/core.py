from pydantic import BaseModel, create_model
from sentinel.models.database import Database
from sentinel.utils.logger import get_logger


class CoreMonitoredAddressDB:
    name = "monitored_address"

    def __init__(self, name: str, network: str, model: BaseModel = None) -> None:
        self.name = name if name else self.name
        self.network = network
        self.model: BaseModel = create_model(
            "MonitoredAddressModel",
            monitored_address=(str, None),
            config_id=(int, None),
            config=(BaseModel, None),
            __base__=model,
        )

        self.logger = get_logger(__name__)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            **kwargs,
        )

    def update(self) -> None: ...
