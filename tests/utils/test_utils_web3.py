from unittest.mock import AsyncMock, patch

import pytest
from web3 import AsyncWeb3

from sentinel.utils.web3 import get_async_web3


@pytest.mark.asyncio
async def test_get_async_web3():
    rpc_url = "http://localhost:8545"

    with patch("sentinel.utils.web3.AsyncWeb3") as MockAsyncWeb3:
        mock_web3_instance = AsyncMock(spec=AsyncWeb3)
        mock_web3_instance.manager = AsyncMock()
        MockAsyncWeb3.return_value = mock_web3_instance
        mock_web3_instance.provider.endpoint_uri = rpc_url
        mock_web3_instance.manager.coro_request.return_value = {"eth": "1.0"}

        web3_instance = get_async_web3(rpc_url)

        assert isinstance(web3_instance, AsyncWeb3), "The returned instance is not of type AsyncWeb3"
        assert web3_instance.provider.endpoint_uri == rpc_url, "The RPC URL does not match"
        assert "eth" in await web3_instance.manager.coro_request("rpc_modules", []), "The 'eth' module is not available"
