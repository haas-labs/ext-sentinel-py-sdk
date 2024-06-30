import os
import pathlib
import sqlite3
from typing import Dict, Iterator, Optional, Union

from pydantic import BaseModel


class Database:
    def __init__(self, path: Union[str, pathlib.Path], overwrite: bool = False) -> None:
        self.path = path
        if isinstance(self.path, str) and self.path == ":memory:":
            self.conn = sqlite3.connect(":memory:")
            return
        self.path = pathlib.Path(self.path)
        if overwrite is True and path.exists():
            os.remove(self.path)
        self.conn = sqlite3.connect(self.path)

    def __repr__(self) -> str:
        return "Database({})".format(self.path)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def query(self, sql: str, params: Optional[Union[Iterator, dict]] = None) -> Iterator[BaseModel]:
        """
        Execute ``sql`` and return an iterable of dictionaries representing each row.

        :param sql: SQL query to execute
        :param params: Parameters to use in that query - an iterable for ``where id = ?``
          parameters, or a dictionary for ``where id = :id``
        """
        cursor = self.execute(sql, params or tuple())
        keys = [d[0] for d in cursor.description]
        for row in cursor:
            yield dict(zip(keys, row))

    def execute(self, sql: str, parameters: Optional[Union[Iterator, dict]] = None) -> sqlite3.Cursor:
        """
        Execute SQL query and return a ``sqlite3.Cursor``.

        :param sql: SQL query to execute
        :param parameters: Parameters to use in that query - an iterable for ``where id = ?``
          parameters, or a dictionary for ``where id = :id``
        """
        if parameters is not None:
            return self.conn.execute(sql, parameters)
        else:
            return self.conn.execute(sql)

    def vacuum(self):
        self.execute("VACUUM;")

    def analyze(self, name=None):
        """
        Run ``ANALYZE`` against the entire database or a named table or index.

        :param name: Run ``ANALYZE`` against this specific named table or index
        """
        self.execute("ANALYZE" if name is None else f"ANALYZE [{name}]")

    @property
    def version(self) -> Dict[str, str]:
        """
        returns versions
        """
        row = self.execute("select sqlite_version()").fetchone()[0]
        return {"sqlite": row}

    @property
    def journal_mode(self) -> str:
        """
        returns current journal_mode of this database.

        https://www.sqlite.org/pragma.html#pragma_journal_mode
        """
        return self.execute("PRAGMA journal_mode;").fetchone()[0]

    def enable_wal(self):
        """
        Sets ``journal_mode`` to ``'wal'`` to enable Write-Ahead Log mode.
        """
        if self.journal_mode != "wal":
            self.execute("PRAGMA journal_mode=wal;")

    def disable_wal(self):
        "Sets ``journal_mode`` back to ``'delete'`` to disable Write-Ahead Log mode."
        if self.journal_mode != "delete":
            self.execute("PRAGMA journal_mode=delete;")
