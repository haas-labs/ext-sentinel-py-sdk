import asyncio

from sentinel.core.v2.channel import Channel, OutboundChannel
from sentinel.metrics.registry import Registry
from sentinel.utils.logger import get_logger

DEFAULT_PUSH_INTERVAL = 10


class OutboundMetricChannel(OutboundChannel):
    name = "metrics"

    def __init__(
        self,
        id: str,
        registry: Registry,
        monitoring_port: int = 9090,
        push_interval: int = DEFAULT_PUSH_INTERVAL,
        name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(id=id, name=name, record_type="sentinel.metrics.collector.MetricModel", **kwargs)
        self._monitoring_port = monitoring_port
        self._push_interval = push_interval

        assert registry is not None, "Undefined registry"
        self._registry = registry

    @classmethod
    def from_settings(cls, settings: Channel, registry: Registry, monitoring_port: int = 9090, **kwargs):
        return cls(
            id=settings.id,
            name=settings.name,
            registry=registry,
            monitoring_port=monitoring_port,
            **kwargs,
        )

    async def run(self):
        self.logger = get_logger(__name__)
        while True:
            for metric in self._registry.dump_all():
                # Add logic to publish metrics via HTTP interface
                await asyncio.sleep(1)
            await asyncio.sleep(self._push_interval)
