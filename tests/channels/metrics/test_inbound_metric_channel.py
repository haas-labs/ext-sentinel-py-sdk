import pytest
from sentinel.channels.metric.core import InboundMetricChannel
from sentinel.core.v2.channel import Channel
from sentinel.metrics.collector import MetricModel, MetricsTypes
from sentinel.metrics.core import MetricQueue


def test_inbound_metric_channel_init():
    channel = InboundMetricChannel(id="metrics/publisher", name="metrics", metric_queue=MetricQueue())
    assert isinstance(channel, InboundMetricChannel), "Incorrect channel type"


def test_inbound_metric_channel_from_settings():
    channel = InboundMetricChannel.from_settings(
        settings=Channel(id="metrics/publisher", type=""), metric_queue=MetricQueue()
    )
    assert isinstance(channel, InboundMetricChannel), "Incorrect channel type"


@pytest.mark.asyncio
async def test_inbound_metric_channel_send():
    queue = MetricQueue()
    total_requests = MetricModel(
        kind=MetricsTypes.counter, name="total_requests", doc="Total requests", timestamp=0, values=0
    )
    channel = InboundMetricChannel.from_settings(
        settings=Channel(
            id="metrics/publisher",
            type="",
        ),
        metric_queue=queue,
    )
    await channel.send(total_requests)

    metric = await queue.receive()
    assert metric == total_requests, "Incorrect metric (total_requests) sent/received"


@pytest.mark.asyncio
async def test_inbound_metric_channel_send_incorrect_metric_type():
    queue = MetricQueue()
    total_requests = {
        "kind": MetricsTypes.counter,
        "name": "total_requests",
        "doc": "Total requests",
        "timestamp": 0,
        "values": 0,
    }
    channel = InboundMetricChannel(id="metrics/publisher", metric_queue=queue)
    with pytest.raises(RuntimeError) as err:
        await channel.send(total_requests)
    assert (
        str(err.value) == "Incorrect metric type, founded: <class 'dict'>, expected: MetricModel"
    ), "Incorrect error message"
