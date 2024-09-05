import csv
import datetime
import pathlib
import time
from typing import List

from sentinel.models.database import Database
from sentinel.utils.logger import get_logger

from .common import Contract


class MonitoredContractsDB:
    name = "monitored_contract"

    def __init__(self, path: pathlib.Path, network: str, update_interval: int = 300) -> None:
        """
        Static Monitored Constacts Database Init
        """
        self.logger = get_logger(__name__)

        # The path to local static monitored contracts DB
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        self.network = network

        self._contracts = []

        self._last_update = self.current_time()
        self._update_interval = update_interval

        if self.path.suffix == ".csv":
            self._import_csv(self.path)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        network = settings.parameters.pop("network")
        kwargs.update(settings.parameters)
        return cls(
            network=network,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )

    def current_time(self):
        """
        returns current time in epoch time (seconds)
        """
        return int(time.time())

    def _import_csv(self, path: pathlib.Path) -> None:
        """
        Import Mixer DB from csv file
        """
        reader = csv.DictReader(path.open("r"))
        for row in reader:
            contract = Contract(**row)
            if contract.network == self.network:
                self._contracts.append(contract.contract_address.lower())
        self.logger.info(f"Imported {len(self.contracts)} monitored contracts")
        self._contracts = list(set(self._contracts))

    async def update(self) -> None:
        """
        Update Local Monitored Contracts list

        interval: will trigger update every N secs
        """
        time_interval_between_updates = self.current_time() - self._last_update
        if len(self.contracts) > 0 and (time_interval_between_updates < self._update_interval):
            return self.contracts

        self._last_update = self.current_time()
        last_update_dt = datetime.datetime.fromtimestamp(self._last_update).isoformat()
        self.logger.info(f"Detected monitored contract: {len(self.contracts)}, last update: {last_update_dt}")

        self._import_csv(self.path)

    @property
    def contracts(self) -> List[Contract]:
        """
        returns the list of contracts
        """
        return self._contracts

    def exists(self, address: str) -> bool:
        """
        returns True if address is in monitored contracts list
        """
        address = address.lower() if address is not None else address
        if address in self._contracts:
            return True
        else:
            return False
