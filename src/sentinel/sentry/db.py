import logging

from typing import List, Dict
from sentinel.utils.imports import import_by_classpath

logger = logging.getLogger(__name__)


class SentryDatabases:
    def __init__(self, aliases: List[str], settings: Dict) -> None:
        self._databases = []
        for db in settings.get("databases", []):
            if db.get("alias") in aliases:
                self._load_db(db)

    @property
    def databases(self):
        return self._databases

    def _load_db(self, db: Dict) -> None:
        db_alias = db.get("alias")
        try:
            db_type = db.get("type")
            db_parameters = db.get("parameters", {})
            logger.info(f"Initializing database: {db_alias}, type: {db_type}")
            _, db_class = import_by_classpath(db_type)
            db_instance = db_class(**db_parameters)
            setattr(self, db_instance.name, db_instance)
            self._databases.append(db_instance.name)
        except AttributeError as err:
            logger.error(f"{db_alias} -> Database initialization issue, {err}")
