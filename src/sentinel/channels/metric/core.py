from sentinel.utils.logger import get_logger

from sentinel.channels.common import Channel

from sentinel.metrics.core import MetricQueue
from sentinel.metrics.collector import MetricModel


class MetricChannel(Channel):
    name = "metrics"

    def __init__(self, name: str, record_type: str, metric_queue: MetricQueue, **kwargs) -> None:
        super().__init__(name, record_type, **kwargs)
        self._queue = metric_queue
        self.logger = get_logger(__name__)

    async def run(self) -> None:
        self.logger.info(f"{self.name} -> Starting consuming metrics")
        try:
            while True:
                metric = await self._queue.receive()
                await self.on_metric(metric)
        finally:
            self.logger.info("Closing metrics channel")

    async def send(self, metric: MetricModel) -> None:
        await self._queue.send(metrics=metric)

    async def on_metric(self, metric: MetricModel) -> None: ...
