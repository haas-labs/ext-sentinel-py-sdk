from collections import defaultdict
from typing import Dict

from pydantic import BaseModel, Field
from sentinel.models.database import Database
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import get_logger


class Target(BaseModel):
    address: str
    config_id: int
    config: Dict = Field(default_factory=dict)


class CoreTargetDB:
    name = "target"

    def __init__(self, name: str, sentry_name: str, sentry_hash: str, network: str, model: str = None) -> None:
        self.name = name if name else self.name
        self.sentry_name = sentry_name
        self.sentry_hash = sentry_hash
        self.network = network

        self.logger = get_logger(__name__)

        if model is not None and model != "":
            _, model = import_by_classpath(model)

        # Target Database
        # The structure: <address> -> <conditions>
        self._db: Dict[str, Dict] = defaultdict()

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
    def size(self):
        return len(self._address_db)

    def update(self, target: Target) -> None:
        self._db[target.address] = target.config

    def has_address(self, address: str) -> bool:
        return True if address in self._db else False
