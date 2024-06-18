import datetime
import time
from typing import List

import httpx
from sentinel.models.database import Database
from sentinel.utils.logger import get_logger

from .common import Contract

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class MonitoredContractsDB:
    name = "monitored_contract"

    def __init__(
        self,
        endpoint_url: str,
        token: str,
        network: str = "ethereum",
        update_interval: int = 300,
        **kwargs,
    ) -> None:
        """
        Monitored Constacts Database Init
        """
        self.logger = get_logger(__name__)

        self._endpoint_url = endpoint_url
        self._token = token

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"

        self._network = network
        self._contracts = []

        # The flag for tracking first database update
        self._initial_update = True

        self._last_update = self.current_time()
        self._update_interval = update_interval

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        endpoint_url = settings.parameters.get("endpoint_url")
        token = settings.parameters.get("token")
        network = settings.parameters.get("network")
        update_interval = settings.parameters.get("update_interval")
        kwargs.update(settings.parameters)
        return cls(
            endpoint_url=endpoint_url,
            token=token,
            network=network,
            update_interval=update_interval,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )

    def current_time(self):
        """
        returns current time in epoch time (seconds)
        """
        return int(time.time())

    async def update(self) -> List[Contract]:
        """
        Update Local Monitored Contracts list

        interval: will trigger update every N secs
        """
        time_interval_between_updates = self.current_time() - self._last_update
        if not self._initial_update and (time_interval_between_updates < self._update_interval):
            return self.contracts

        self._last_update = self.current_time()
        query = {"size": 10000}
        endpoint = self._endpoint_url + "/api/v1/contract/search"

        async with httpx.AsyncClient(verify=False) as httpx_async_client:
            response = await httpx_async_client.post(url=endpoint, headers=self._headers, json=query)
        if response.status_code == 200:
            data = response.json().get("data", [])
            # extract only required contract fields
            self._contracts = [
                contract.get("address").lower() for contract in data if contract.get("chainUid") == self._network
            ]
            # remove duplicates
            self._contracts = list(set(self._contracts))

            last_update_dt = datetime.datetime.fromtimestamp(self._last_update).isoformat()
            self.logger.info(f"Detected monitored contracts: {len(self.contracts)}, last update: {last_update_dt}")
            self._initial_update = False
            return self._contracts

        elif response.status_code == 404:
            return []
        else:
            raise RuntimeError(f"Request error, status code: {response.status_code}, response: {response}")

    @property
    def contracts(self) -> List[str]:
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
