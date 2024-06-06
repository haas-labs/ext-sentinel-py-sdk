import pytest
from sentinel.channels.metric.core import InboundMetricChannel
from sentinel.core.v2.channel import Channel
from sentinel.metrics.collector import MetricModel, MetricsTypes
from sentinel.metrics.core import MetricQueue


def test_inbound_metric_channel_init():
    channel = InboundMetricChannel(id="metrics/consumer", name="metrics", queue=MetricQueue())
    assert isinstance(channel, InboundMetricChannel), "Incorrect channel type"


def test_inbound_metric_channel_from_settings():
    channel = InboundMetricChannel.from_settings(
        settings=Channel(id="metrics/consumer", type=""), metrics_queue=MetricQueue()
    )
    assert isinstance(channel, InboundMetricChannel), "Incorrect channel type"


@pytest.mark.asyncio
async def test_inbound_metric_channel_send():
    class MetricsConsumer(InboundMetricChannel):
        def __init__(self, id: str, queue: MetricQueue, name: str = None, **kwargs) -> None:
            super().__init__(id=id, queue=queue, name=name, **kwargs)
            self.metrics = list()

        async def on_metric(self, metric: MetricModel):
            self.metrics.append(metric)

    queue = MetricQueue()
    total_requests = MetricModel(
        kind=MetricsTypes.counter, name="total_requests", doc="Total requests", timestamp=0, values=0
    )
    channel = MetricsConsumer.from_settings(
        settings=Channel(id="metrics/consumer", type="", parameters={"stop_after": 1}),
        metrics_queue=queue,
    )
    # await queue.send(total_requests)
    queue.send(total_requests)
    await channel.run()

    assert len(channel.metrics) == 1, "Incorrect metrics number"
    assert channel.metrics[0] == total_requests, "Received incorrect total requests metric"
