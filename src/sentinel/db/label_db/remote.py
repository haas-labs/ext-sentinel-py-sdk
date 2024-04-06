import httpx

from typing import List

from .common import CommonLabelDB
from .common import LabelDBRecord


DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class LabelDB(CommonLabelDB):
    name = "label"

    def __init__(
        self,
        endpoint_url: str,
        token: str,
        chain_id: str,
        network: str,
        update_tags: List[str] = [],
        update_interval: int = 120,
        **kwargs,
    ) -> None:
        """
        Label DB Init
        """
        super().__init__(update_tags=update_tags, update_interval=update_interval)

        self._endpoint_url = endpoint_url
        self._token = token

        self._chain_id = chain_id
        self._network = network

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"

    async def search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]:
        """
        Search labeles for specific addresses and tags
        """
        uniq_addresses = list()
        query = {
            "addresses": addresses,
            "tags": tags,
            # "blockchainNetwork": self._network,
        }
        endpoint = self._endpoint_url + "/api/v2/label/cached"

        async with httpx.AsyncClient(verify=False) as httpx_async_client:
            response = await httpx_async_client.post(url=endpoint, headers=self._headers, json=query)
        if response.status_code == 200:
            results = []
            label_db_record_fields = LabelDBRecord.model_fields.keys()
            for record in response.json().get("data", []):
                # addresses deduplication
                record_address = record.get("address")
                if record_address in uniq_addresses:
                    continue
                uniq_addresses.append(record_address)

                record = {k: v for k, v in record.items() if k in label_db_record_fields}
                results.append(LabelDBRecord(**record))
            return results

        elif response.status_code == 404:
            return []
        else:
            raise RuntimeError(
                f"Request error, status code: {response.status_code}, "
                + f"response: {response.content}, query: {query}"
            )

    async def search_by_tag(self, tags: List[str], from_pos: int = 0, limit: int = 15000) -> List[LabelDBRecord]:
        """
        Search labeles by tags
        """
        uniq_addresses = list()
        query = {
            "from": from_pos,
            "size": limit,
            "where": "tags in ({})".format(",".join([f"'{t}'" for t in tags])),
        }
        endpoint = self._endpoint_url + "/api/v2/label/search"

        async with httpx.AsyncClient(verify=False) as httpx_async_client:
            response = await httpx_async_client.post(url=endpoint, headers=self._headers, json=query)
        if response.status_code == 200:
            results = []
            label_db_record_fields = LabelDBRecord.model_fields.keys()
            for record in response.json().get("data", []):
                # addresses deduplication
                record_address = record.get("address")
                if record_address in uniq_addresses:
                    continue
                uniq_addresses.append(record_address)

                record = {k: v for k, v in record.items() if k in label_db_record_fields}
                results.append(LabelDBRecord(**record))
            return results

        elif response.status_code == 404:
            return []
        else:
            raise RuntimeError(
                f"Request error, status code: {response.status_code}, "
                + f"response: {response.content}, query: {query}"
            )

    async def add(self, address: str, tags: List[str], category: str) -> bool:
        """
        add address to label db
        """
        await super().add(address=address, tags=tags, category=category)

        parameters = {
            "create": {
                "tags": tags,
                "category": category,
            },
            "update": {
                "tags": tags,
            },
        }
        endpoint = self._endpoint_url + f"/api/v2/blockchain/{self._network}/address/{address}/label/upsert"

        async with httpx.AsyncClient(verify=False) as httpx_async_client:
            response = await httpx_async_client.post(url=endpoint, headers=self._headers, json=parameters)
        if response.status_code != 201:
            self.logger.error(
                f"Cannot add address to label DB, status: {response.status_code}, "
                + f"network: {self._network}, address: {address}, parameters: {parameters}, "
                + f"response: {response.content}"
            )
            return False
        return True
