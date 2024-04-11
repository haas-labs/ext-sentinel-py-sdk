import asyncio


class Metrics: ...


class MetricQueue:
    def __init__(self):
        self._metrics_queue = asyncio.Queue()

    async def send(self, metrics: Metrics) -> None:
        await self._metrics_queue.put(metrics)

    async def receive(self) -> Metrics:
        return await self._metrics_queue.get()
