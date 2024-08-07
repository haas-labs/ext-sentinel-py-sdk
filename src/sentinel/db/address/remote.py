import httpx
from sentinel.db.address.common import CommonAddressDB
from sentinel.models.address import AddressType
from sentinel.models.database import Database

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class RemoteAddressDB(CommonAddressDB):
    name = "address"

    def __init__(
        self,
        endpoint_url: str,
        token: str,
        chain_id: int,
        network: str,
        timeout: int = 60,
        **kwargs,
    ) -> None:
        """
        Address DB Init
        """
        super().__init__()

        self._endpoint = endpoint_url + "/api/v2/contract/fetch"
        self._timeout = timeout

        self._chain_id = chain_id
        self._network = network

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {token}"

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        endpoint_url = settings.parameters.pop("endpoint_url")
        token = settings.parameters.pop("token")
        chain_id = settings.parameters.pop("chain_id")
        network = settings.parameters.pop("network")
        timeout = settings.parameters.pop("timeout", 60)
        kwargs.update(settings.parameters)
        return cls(
            endpoint_url=endpoint_url,
            token=token,
            chain_id=chain_id,
            network=network,
            timeout=timeout,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )

    async def _fetch(self, address: str) -> AddressType:
        """
        fetch address details: address/contract
        """
        query = {
            "networkUid": self._network,
            "address": address,
        }

        async with httpx.AsyncClient(verify=False) as httpx_async_client:
            response = await httpx_async_client.post(url=self._endpoint, headers=self._headers, json=query)

        match response.status_code:
            case 200:
                data = response.json()
                if data.get("abi", None) is not None:
                    return AddressType.contract
                else:
                    return AddressType.undefined
            case 404:
                raise NotImplementedError()
            case _:
                raise RuntimeError(
                    f"Request error, status code: {response.status_code}, "
                    + f"response: {response.content}, query: {query}"
                )
