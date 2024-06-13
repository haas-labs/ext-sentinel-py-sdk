from pydantic import BaseModel
from sentinel.models.database import Database


class CoreConfigDB:
    def __init__(self, model: BaseModel) -> None:
        # TODO add to model monitored address
        self.model = model

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        return cls(settings, **kwargs)

    def update(self) -> None: ...
