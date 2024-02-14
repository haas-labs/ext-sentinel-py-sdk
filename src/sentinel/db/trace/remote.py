import logging

from .common import CommonTraceDB

from sentinel.formats.trace import Trace
from sentinel.services.rpc.tracer import Tracer


logger = logging.getLogger(__name__)


class RemoteTraceDB(CommonTraceDB):
    """
    Remote Trace DB
    """

    def __init__(self, endpoint_url: str, network: str, timeout: int = 60) -> None:
        '''
        Remote Trace DB Init
        '''
        self.tracer = Tracer(endpoint=endpoint_url, network=network, timeout=timeout)

    async def get(self, tx_hash: str) -> Trace:
        """
        returns a trace by transaction hash
        """
        trace = await self.tracer.get(tx_hash=tx_hash)
        return Trace(data=trace)
