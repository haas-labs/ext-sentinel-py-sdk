import pathlib

from sentinel.core.v2.sentry import Sentry as SentryInstance
from sentinel.db.core.common import Database as CommonDatabase
from sentinel.models.database import Database as DatabaseSettings
from sentinel.utils.logger import get_logger


class Database:
    name = "database"

    def __init__(
        self,
        name: str,
        sentry: SentryInstance,
        db_path: pathlib.Path | str = ":memory:",
        db_mode: str = "overwrite",
    ) -> None:
        self.name = name if name else self.name
        self.sentry = sentry

        self.logger = sentry.logger if getattr(sentry, "logger", None) is not None else get_logger(__name__)

        self._db = CommonDatabase(path=":memory:")

    @classmethod
    def from_settings(cls, settings: DatabaseSettings, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        kwargs.update(settings.parameters)
        return cls(
            name=settings.name,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )
