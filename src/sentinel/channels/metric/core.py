import asyncio

from sentinel.core.v2.channel import Channel, InboundChannel, OutboundChannel
from sentinel.metrics.collector import MetricModel
from sentinel.metrics.core import MetricQueue
from sentinel.utils.logger import get_logger

DEFAULT_TIMEOUT = 10


class OutboundMetricChannel(OutboundChannel):
    name = "metrics"

    def __init__(self, id: str, metric_queue: MetricQueue, name: str = None, **kwargs) -> None:
        super().__init__(id=id, name=name, record_type="sentinel.metrics.collector.MetricModel", **kwargs)
        self._queue = metric_queue
        self.logger = get_logger(__name__)

    @classmethod
    def from_settings(cls, settings: Channel, **kwargs):
        metric_queue = kwargs.pop("metric_queue", None)
        return cls(
            id=settings.id,
            name=settings.name,
            metric_queue=metric_queue,
            **kwargs,
        )

    async def run(self):
        while True:
            await asyncio.sleep(DEFAULT_TIMEOUT)

    async def send(self, metric: MetricModel) -> None:
        if not isinstance(metric, MetricModel):
            raise RuntimeError(f"Incorrect metric type, founded: {type(metric)}, expected: MetricModel")
        else:
            await self._queue.send(metrics=metric)


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
