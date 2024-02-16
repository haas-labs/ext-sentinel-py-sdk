import json
import aiofiles
import pathlib
import logging

from typing import List

from .common import CommonLabelDB
from .common import LabelDBRecord


logger = logging.getLogger(__name__)


def touch(path: pathlib.Path) -> None:
    """
    similar to `touch` unix command
    """
    if isinstance(path, str):
        path = pathlib.Path(path)

    path.open("a").close()


class LabelDB(CommonLabelDB):
    """
    Label DB
    """

    def __init__(
        self,
        path: pathlib.Path,
        update_tags: List[str] = [],
        update_interval: int = 120,
        **kwargs,
    ) -> None:
        """
        Label DB Init
        """
        super().__init__(update_tags=update_tags, update_interval=update_interval)

        self.path = path
        touch(self.path)

    async def search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]:
        """
        Search labels by tag(-s)
        """
        results = []
        async with aiofiles.open(self.path, "r") as db:
            async for raw_record in db:
                record = LabelDBRecord(**json.loads(raw_record))
                for tag in record.tags:
                    if tag not in tags:
                        continue
                    results.append(record)
        return results

    async def search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]:
        """
        Search labels by address(-es)
        """
        results = []
        async with aiofiles.open(self.path, "r") as db:
            async for raw_record in db:
                record = LabelDBRecord(**json.loads(raw_record))
                if record.address not in addresses:
                    continue
                for tag in record.tags:
                    if tag not in tags:
                        continue
                    results.append(record)
        return results

    async def add(self, address: str, tags: List[str], category: str) -> bool:
        """
        add address to label db
        """
        await super().add(address=address, tags=tags, category=category)

        search_result = await self.search_by_address(addresses=[address], tags=tags)
        if len(search_result) == 0:
            async with aiofiles.open(self.path, "a") as db:
                record = json.dumps(
                    {
                        "address": address,
                        "tags": list(set(tags)),
                        "category": category,
                    }
                )
                await db.write(f"{record}\n")
        return True
