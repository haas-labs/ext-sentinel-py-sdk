from collections import defaultdict
from typing import Dict

from pydantic import BaseModel, Field, create_model

from sentinel.models.database import Database
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger


class Config(BaseModel):
    address: str
    parameters: Dict = Field(default_factory=dict)


class CoreMonitoringConfigDB:
    name = "monitoring_config"

    def __init__(self, name: str, sentry_name: str, sentry_hash: str, network: str, model: str = None) -> None:
        self.name = name if name else self.name
        self.sentry_name = sentry_name
        self.sentry_hash = sentry_hash
        self.network = network
        if model is not None or model != "":
            _, model = import_by_classpath(model)

        self.model: BaseModel = create_model(
            "MonitoringConfigModel",
            monitored_address=(str, None),
            monitoring_id=(int, None),
            configs=(BaseModel, None),
            __base__=model,
        )

        self.logger = get_logger(__name__)

        # Monitored Address Database
        # The structure: <address> -> <conditions>
        self._address_db: Dict[str, Dict] = defaultdict()

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

    @property
    def size(self) -> int:
        return len(self._address_db)

    def update(self, config: Config) -> None:
        """
        update config(-s) in database
        """
        self._address_db[config.address] = config.parameters

    def has_address(self, address: str) -> bool:
        """
        returns True if address is in database
        """
        return True if address in self._address_db else False
