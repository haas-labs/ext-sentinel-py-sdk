import time
import datetime

from typing import List, Dict

from pydantic import BaseModel

from sentinel.utils.logger import get_logger


class LabelDBRecord(BaseModel):
    address: str
    tags: List[str]
    category: str


class CommonLabelDB:
    name = "label"

    def __init__(self, update_tags: List[str] = list(), update_interval: int = 120):
        """
        Common Label DB Init

        @param update_tags      the list of tags for updating
        @param update_interval  time between updates in seconds, default: 120 secs
        """
        self.logger = get_logger(__name__)
        # Local database for storing addresses by tag
        self._addresses = {tag: list() for tag in update_tags}
        self._addresses_updated = False

        self._last_update = self.current_time()
        self._update_interval = update_interval

    @property
    def stats(self) -> Dict:
        """
        returns stats for local addresses by tags
        """
        return {k: len(v) for k, v in self._addresses.items()}

    def current_time(self):
        """
        returns current time in epoch time (seconds)
        """
        return int(time.time())

    async def search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]:
        """
        Search by tag(-s)
        """
        raise NotImplementedError()

    async def search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]:
        """
        Search by address(-es)
        """
        raise NotImplementedError()

    async def add(self, address: str, tags: List[str], category: str) -> bool:
        """
        Add address to label db
        """
        for tag in tags:
            if tag not in self._addresses:
                continue
            if address not in self._addresses.get(tag, []):
                self._addresses[tag].append(address)
        return True

    async def update(self):
        """
        Update local address db for predefined tags
        """
        time_interval_between_updates = self.current_time() - self._last_update
        if self._addresses_updated and (time_interval_between_updates < self._update_interval):
            return

        self._last_update = self.current_time()
        last_update_dt = datetime.datetime.fromtimestamp(self._last_update).isoformat()
        self.logger.info(f"Updating label database, last update: {last_update_dt}, records: {self.stats()}")

        for tag in self._addresses.keys():
            try:
                addresses = [r.address for r in await self.search_by_tag(tags=[tag])]
                if len(addresses) > 0:
                    self._addresses[tag] = list(set(addresses))
            except RuntimeError as err:
                self.logger.error(err)
        self._addresses_updated = True

    def has_tag(self, address: str, tag: str) -> bool:
        """
        Returns True if the address has the tag
        """
        if tag not in self._addresses:
            return False

        if address in self._addresses.get(tag, []):
            return True
        else:
            return False
