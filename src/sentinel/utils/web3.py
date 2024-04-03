from web3 import Web3
from web3.eth import AsyncEth


def get_async_web3(
    rpc_url: str,
) -> Web3:
    """
    return Async Web3 Interface
    """
    return Web3(Web3.AsyncHTTPProvider(rpc_url), modules={"eth": (AsyncEth,)}, middlewares=[])
