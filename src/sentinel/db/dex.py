import pathlib
from typing import List

from sentinel.utils.logger import get_logger


class LocalDEXAddresses:
    name = "dex"

    def __init__(self, path: pathlib.Path) -> None:
        """
        Local DEX Address Database Init
        """
        self.logger = get_logger(__name__)
        # The path to local DEX Addresses
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        self._db = []
        self._import(self.path)

    def _import(self, path: pathlib.Path) -> None:
        """
        Import DEX Address DB from file
        """
        path = pathlib.Path(path) if isinstance(path, str) else path
        with path.open("r", encoding="utf-8") as source:
            for address in source:
                if not address:
                    continue
                if address.startswith("0x"):
                    self._db.append(address.strip())

        self._db = list(set(self._db))
        self.logger.info(f"Imported {len(self._db)} DEX addresses")

    def exists(self, address: str) -> bool:
        """
        returns True if address is in DEX list
        """
        if address in self._db:
            return True
        else:
            return False

    def all(self) -> List[str]:
        """
        returns all DEX addresses in local storage
        """
        return self._db
