import pathlib

from sentinel.utils.logger import get_logger


class LocalBlacklistDB:
    name = "blacklist"

    def __init__(self, path: pathlib.Path) -> None:
        """
        Local Blacklist Database Init
        """
        self.logger = get_logger(__name__)

        # The path to local blacklist DB
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        self._db = []
        self._import(self.path)

    def _import(self, path: pathlib.Path) -> None:
        """
        Import Blacklist DB from file
        """
        path = pathlib.Path(path) if isinstance(path, str) else path
        with path.open("r", encoding="utf-8") as source:
            for address in source:
                if not address:
                    continue
                if address.startswith("0x"):
                    self._db.append(address.strip())

        self._db = list(set(self._db))
        self.logger.info(f"Imported {len(self._db)} blacklist records")

    def exists(self, address: str) -> bool:
        """
        returns True if address is in blacklist list
        """
        if address in self._db:
            return True
        else:
            return False
