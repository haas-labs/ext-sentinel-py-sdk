import csv
import pathlib

from pydantic import BaseModel

from sentinel.utils.logger import get_logger


class MixerRecord(BaseModel):
    """
    Mixer Record
    """

    address: str
    network_id: int


class Mixers:
    name = "mixer"

    def __init__(self, path: pathlib.Path, allowed_chain_id: int) -> None:
        """
        Mixers Init
        """
        self.logger = get_logger(__name__)

        # The path to local mixers DB
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        self.allowed_chain_id = allowed_chain_id

        # The list of mixers
        # TODO add selection by network
        self._db = []

        if self.path.suffix == ".csv":
            self._import_csv(self.path)

    def _import_csv(self, path: pathlib.Path) -> None:
        """
        Import Mixer DB from csv file
        """
        reader = csv.DictReader(path.open("r"))
        for row in reader:
            row = MixerRecord(**row)
            if row.network_id == self.allowed_chain_id:
                self._db.append(row.address)
        self.logger.info(f"Imported {len(self._db)} mixer records")

    def is_mixer(self, address: str) -> bool:
        """
        returns True if address is in mixers list
        """
        if address in self._db:
            return True
        else:
            return False
