from web3 import AsyncWeb3
from web3.eth import AsyncEth


def get_async_web3(rpc_url: str) -> AsyncWeb3:
    """
    return Async Web3 Interface
    """
    return AsyncWeb3(
        provider=AsyncWeb3.AsyncHTTPProvider(rpc_url),
        modules={"eth": (AsyncEth,)},
        middleware=[],
    )
