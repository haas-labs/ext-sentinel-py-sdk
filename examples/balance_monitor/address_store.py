import logging
import pathlib


logger = logging.getLogger(__name__)

class AddressStore:
    def __init__(self, path: pathlib.Path) -> None:
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path
        
        self._db = []
        self._import(self.path)

    def _import(self, path: pathlib.Path) -> None:
        path = pathlib.Path(path) if isinstance(path, str) else path
        with path.open('r', encoding='utf-8') as source:
            for address in source:
                if not address:
                    continue
                if address.startswith('0x'):
                    self._db.append(address.strip())

        self._db = list(set(self._db))
        logger.info(f'Imported {len(self._db)} addresses')

    def exists(self, address: str) -> bool:
        if address.lower() in self._db:
            return True
        else:
            return False

    def all(self) -> list:
        return self._db
