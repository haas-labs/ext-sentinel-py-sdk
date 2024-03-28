from typing import List

from sentinel.models.database import Database

from sentinel.utils.logger import get_logger
from sentinel.utils.imports import import_by_classpath


class SentryDatabases:
    def __init__(self, ids: List[str], databases: List[Database]) -> None:
        self.logger = get_logger(__name__)
        self._databases = []

        if len(ids) > 0:
            self.logger.info(f"Database(-s) activation: {ids}")
        for db in databases:
            if db.id in ids:
                self._load_db(db)
        if len(self._databases) != len(ids): 
            raise RuntimeError(f"Databases mismatch, expected: {sorted(ids)}, activated: {sorted(self._databases)}")


    @property
    def names(self):
        return self._databases

    def _load_db(self, db: Database) -> None:
        try:
            db_parameters = db.parameters
            self.logger.info(f"Initializing database: {db.id}, type: {db.type}")
            _, db_class = import_by_classpath(db.type)
            db_instance = db_class(**db_parameters)
            setattr(self, db_instance.name, db_instance)
            self._databases.append(db_instance.name)
        except AttributeError as err:
            self.logger.error(f"Database initialization issue, database id: {db.id}, error: {err}")
