import pathlib

from sentinel.models.database import Database
from sentinel.utils.logger import get_logger


class AddressDB:
    name = "address"

    def __init__(self, path: pathlib.Path, **kwargs) -> None:
        self.logger = get_logger(__name__)
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        self._db = []
        self._import(self.path)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        path = settings.parameters.pop("path")
        kwargs.update(settings.parameters)
        return cls(path=path, **kwargs)

    def _import(self, path: pathlib.Path) -> None:
        path = pathlib.Path(path) if isinstance(path, str) else path
        with path.open("r", encoding="utf-8") as source:
            for address in source:
                address = address.lower().strip()
                if not address:
                    continue
                if address.startswith("0x"):
                    self._db.append(address.strip().lower())

        self._db = list(set(self._db))
        self.logger.info("AddressDB: {}".format({"imported_addresses": len(self._db), "path": self.path}))

    def exists(self, address: str) -> bool:
        if not address:
            return False
        if address.lower() in self._db:
            return True
        else:
            return False

    def all(self) -> list:
        return self._db
