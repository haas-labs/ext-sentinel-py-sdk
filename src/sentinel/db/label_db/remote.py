from typing import Dict, List

import httpx

from sentinel.models.database import Database

from .common import CommonLabelDB, LabelDBRecord

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

RECORDS_PER_REQUEST = 10000


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

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        endpoint_url = settings.parameters.pop("endpoint_url")
        token = settings.parameters.pop("token")
        chain_id = settings.parameters.pop("chain_id")
        network = settings.parameters.pop("network")
        update_tags = settings.parameters.pop("update_tags", [])
        update_interval = settings.parameters.pop("update_interval", 120)
        kwargs.update(settings.parameters)
        return cls(
            endpoint_url=endpoint_url,
            token=token,
            chain_id=chain_id,
            network=network,
            update_tags=update_tags,
            update_interval=update_interval,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )

    async def query(self, endpoint: str, query: Dict, fetch_all: bool = False) -> List[LabelDBRecord]:
        """
        Run query agains LabelDB
        """
        uniq_addresses = list()

        async def _query(endpoint: str, query: str) -> List[LabelDBRecord]:
            label_db_record_fields = LabelDBRecord.model_fields.keys()
            records = []
            async with httpx.AsyncClient(verify=False) as httpx_async_client:
                response = await httpx_async_client.post(url=endpoint, headers=self._headers, json=query)
            if response.status_code == 200:
                resp = response.json()
                data = resp.get("data", [])
                for record in data:
                    # addresses deduplication
                    record_address = record.get("address")
                    if record_address in uniq_addresses:
                        continue
                    uniq_addresses.append(record_address)

                    record = {k: v for k, v in record.items() if k in label_db_record_fields}
                    records.append(LabelDBRecord(**record))
                return records

            elif response.status_code == 404:
                return records
            else:
                raise RuntimeError(
                    f"Request error, status code: {response.status_code}, "
                    + f"response: {response.content}, query: {query}"
                )

        if not fetch_all:
            return await _query(endpoint=endpoint, query=query)
        else:
            records = []
            query.update(
                {
                    "from": 0,
                    "size": RECORDS_PER_REQUEST,
                }
            )
            while True:
                query_results = await _query(endpoint=endpoint, query=query)
                if len(query_results) == 0:
                    break
                records.extend(query_results)
                query["from"] += RECORDS_PER_REQUEST + 1
            return records

    async def search_by_address(self, addresses: List[str], tags: List[str]) -> List[LabelDBRecord]:
        """
        Search labeles for specific addresses and tags
        """
        endpoint = self._endpoint_url + "/api/v2/label/cached"
        query = {
            "addresses": addresses,
            "tags": tags,
            # "blockchainNetwork": self._network,
        }
        return await self.query(endpoint=endpoint, query=query)

    async def search_by_tag(self, tags: List[str]) -> List[LabelDBRecord]:
        """
        Search labeles by tags
        """
        endpoint = self._endpoint_url + "/api/v2/label/search"
        query = {
            "where": "tags in ({})".format(",".join([f"'{t}'" for t in tags])),
        }
        return await self.query(endpoint=endpoint, query=query, fetch_all=True)

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
        if response.status_code != 200:
            self.logger.error(
                f"Cannot add address to label DB, status: {response.status_code}, "
                + f"network: {self._network}, address: {address}, parameters: {parameters}, "
                + f"response: {response.content}"
            )
            return False
        return True
