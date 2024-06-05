import asyncio

from sentinel.core.v2.channel import Channel, InboundChannel, OutboundChannel
from sentinel.metrics.collector import MetricModel
from sentinel.metrics.core import MetricQueue
from sentinel.metrics.registry import Registry
from sentinel.utils.logger import get_logger

DEFAULT_PUSH_INTERVAL = 10


class OutboundMetricChannel(OutboundChannel):
    name = "metrics"

    def __init__(
        self,
        id: str,
        metric_queue: MetricQueue,
        registry: Registry,
        push_interval: int = DEFAULT_PUSH_INTERVAL,
        name: str = None,
        **kwargs,
    ) -> None:
        super().__init__(id=id, name=name, record_type="sentinel.metrics.collector.MetricModel", **kwargs)
        self.logger = get_logger(__name__)
        self._push_interval = push_interval

        assert metric_queue is not None, "Undefined metrics queue"
        self._queue = metric_queue

        assert registry is not None, "Undefined registry"
        self._registry = registry

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        metric_queue = kwargs.pop("metric_queue", None)
        registry = kwargs.pop("registry", None)
        return cls(
            id=settings.id,
            name=settings.name,
            metric_queue=metric_queue,
            registry=registry,
            **kwargs,
        )

    async def run(self):
        while True:
            for metric in self._registry.dump_all():
                await self._queue.send(metrics=metric)
            await asyncio.sleep(self._push_interval)


class InboundMetricChannel(InboundChannel):
    name = "metrics"

    def __init__(self, id: str, metric_queue: MetricQueue, name: str = None, stop_after: int = 0, **kwargs) -> None:
        super().__init__(id=id, name=name, record_type="sentinel.metrics.collector.MetricModel", **kwargs)
        self._queue = metric_queue
        self.logger = get_logger(__name__)
        self.stop_after = stop_after

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        metric_queue = kwargs.pop("metric_queue", None)
        return cls(
            id=settings.id,
            name=settings.name,
            metric_queue=metric_queue,
            stop_after=settings.parameters.get("stop_after", 0),
            **kwargs,
        )

    async def run(self):
        total_metrics = 0
        while True:
            total_metrics += 1

            metric = await self._queue.receive()
            await self.on_metric(metric)

            if self.stop_after > 0 and total_metrics >= self.stop_after:
                break

    async def on_metric(self, metric: MetricModel) -> None: ...
