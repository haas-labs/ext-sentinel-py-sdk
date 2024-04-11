from enum import Enum
from typing import Dict, Union

import asyncio

from sentinel.metrics import quantile
from sentinel.metrics import histogram

# Types

LabelsType = Dict[str, str]
NumericValueType = Union[int, float, histogram.Histogram, quantile.Estimator]


class MetricsTypes(Enum):
    counter = 0
    gauge = 1
    summary = 2
    untyped = 3
    histogram = 4


class Metrics: ...


class MetricQueue:
    def __init__(self):
        self._metrics_queue = asyncio.Queue()

    async def send(self, metrics: Metrics) -> None:
        await self._metrics_queue.put(metrics)

    async def receive(self) -> Metrics:
        return await self._metrics_queue.get()
