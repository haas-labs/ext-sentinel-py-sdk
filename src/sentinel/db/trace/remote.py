from sentinel.formats.trace import Trace
from sentinel.models.database import Database
from sentinel.services.rpc.tracer import Tracer

from .common import CommonTraceDB


class RemoteTraceDB(CommonTraceDB):
    name = "trace"

    def __init__(self, endpoint_url: str, network: str, timeout: int = 60, **kwargs) -> None:
        """
        Remote Trace DB Init
        """
        self.tracer = Tracer(endpoint=endpoint_url, network=network, timeout=timeout)

    @classmethod
    def from_settings(cls, settings: Database, **kwargs):
        kwargs = kwargs.copy()
        sentry_name = kwargs.pop("sentry_name")
        sentry_hash = kwargs.pop("sentry_hash")
        endpoint_url = settings.parameters.pop("endpoint_url")
        network = settings.parameters.pop("network")
        timeout = settings.parameters.pop("timeout", 60)
        kwargs.update(settings.parameters)
        return cls(
            endpoint_url=endpoint_url,
            network=network,
            timeout=timeout,
            sentry_name=sentry_name,
            sentry_hash=sentry_hash,
            **kwargs,
        )

    async def get(self, tx_hash: str) -> Trace:
        """
        returns a trace by transaction hash
        """
        trace = await self.tracer.get(tx_hash=tx_hash)
        return Trace(data=trace)
