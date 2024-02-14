import json
import httpx
import logging

from typing import Union, List
from async_lru import alru_cache


from sentinel.models.contract import (
    Contract,
    ABISignature,
)
from sentinel.models.errors import EndpointError

from .common import CommonContractDB
from .utils import to_signature_record


logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class RemoteContractDB(CommonContractDB):
    """
    Remote Contract DB
    """

    def __init__(
        self,
        endpoint_url: str,
        token: str,
        network: str,
        chain_id: int,
        timeout: int = 60,
    ) -> None:
        """
        Remote Contract DB Init
        """
        super().__init__(network=network, chain_id=chain_id)

        self.token = token
        self.endpoint = endpoint_url + "/api/v2/contract"
        self.timeout = timeout

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self.token}"

    async def get(
        self, address: str, follow_impl: bool = False
    ) -> Union[Contract, EndpointError]:
        """
        Get contract details
        """
        query = {
            "networkUid": self.network,
            "address": address,
        }

        endpoint_url = self.endpoint + "/fetch"
        try:
            async with httpx.AsyncClient(
                verify=False, timeout=self.timeout
            ) as httpx_async_client:
                response = await httpx_async_client.post(
                    url=endpoint_url, headers=self._headers, json=query
                )
        except httpx.ConnectTimeout:
            logger.warning(f"Connection timeout to {endpoint_url}")
            return None

        if response.status_code == 200:
            contract_data = response.json()
            contract = Contract(**contract_data)
            if follow_impl and contract.implementation is not None:
                return await self.get(address=contract.implementation)
            else:
                return contract
        else:
            data = json.loads(response.content)
            return EndpointError(**data)

    @alru_cache(maxsize=2048)
    async def get_abi_signatures(self, address: str) -> List[ABISignature]:
        """
        returns the list of ABI signatures
        """
        abi_signatures = list()

        contract = await self.get(address=address)
        if not isinstance(contract, Contract):
            logger.warning(f"Contract address: {address}, error: {contract}")
            return []

        if contract.abi is None:
            return []

        for abi_record in contract.abi:
            abi_signatures.append(
                to_signature_record(
                    contract_address=contract.address, abi_record=abi_record
                )
            )

        # Check reference to implementation
        if (
            contract.implementation is not None
            and contract.address != contract.implementation
        ):
            for abi_signature in await self.get_abi_signatures(
                address=contract.implementation
            ):
                abi_signatures.append(abi_signature)

        return abi_signatures
