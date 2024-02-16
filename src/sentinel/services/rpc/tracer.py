import httpx
import logging

from typing import List, Dict


logger = logging.getLogger(__name__)


JSONRPC_VERSION = "2.0"
SUPPORTED_NETWORKS = [
    "ethereum",
    "bsc",
    "arbitrum",
]
HEADERS = {
    "Content-Type": "application/json",
}


class JsonRpcRequest:
    """
    JSON RPC Request
    """

    def __init__(self, method: str, params: List):
        """
        JSON RPC Request Init
        """
        self.data = {
            "jsonrpc": JSONRPC_VERSION,
            "method": method,
            "params": params,
            "id": 1,
        }

    def to_dict(self):
        """
        Transform the request to Dict type
        """
        return self.data


class Tracer:
    """
    Tracer
    """

    def __init__(self, endpoint: str, network: str, timeout: int = 60) -> None:
        """
        Tracer Init
        """
        if network not in SUPPORTED_NETWORKS:
            raise RuntimeError(f"Unsupported network: {network}")

        self.endpoint = endpoint
        self.network = network
        self.timeout = timeout

    async def fetch(self, request: JsonRpcRequest) -> None:
        """
        JSONRPC Fetch
        """
        async with httpx.AsyncClient(verify=False, timeout=self.timeout, follow_redirects=True) as client:
            response = await client.post(
                url=self.endpoint,
                headers=HEADERS,
                json=request.data,
                timeout=self.timeout,
            )

        match response.status_code:
            case 200:
                data = response.json()
                if data.get("error", None) is not None:
                    raise RuntimeError(f"request: {request.data}, response: {data}")
                else:
                    return data.get("result", {})
            case _:
                logger.error(f"RPC Data Fetching error code: {response.status_code}, request: {request.data}")
                logger.error(response.content)
                return {}

    async def get(self, tx_hash: str) -> Dict:
        """
        returns a trace for specified transaction hash
        """
        request = JsonRpcRequest(
            method="debug_traceTransaction",
            params=[
                tx_hash,
                {"tracer": "callTracer"},
            ],
        )
        return await self.fetch(request)

    async def get_latest_block_transactions(self, limit: int = None) -> List[str]:
        """
        returns latest block transactions
        """
        response = await self.fetch(JsonRpcRequest(method="eth_getBlockByNumber", params=["latest", False]))
        if limit is None:
            return response.get("transactions", [])
        else:
            return response.get("transactions", [])[:limit]

    async def get_latest_transaction(self) -> str:
        """
        returns latest block transactions
        """
        transactions = await self.get_latest_block_transactions()
        if len(transactions) > 0:
            return transactions[0]
