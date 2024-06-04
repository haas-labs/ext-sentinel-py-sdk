import pytest
from sentinel.channels.metric.core import OutboundMetricChannel
from sentinel.core.v2.channel import Channel
from sentinel.metrics.collector import MetricModel, MetricsTypes
from sentinel.metrics.core import MetricQueue
from sentinel.metrics.registry import Registry


def test_outbound_metric_channel_init():
    channel = OutboundMetricChannel(
        id="metrics/publisher", name="metrics", metric_queue=MetricQueue(), registry=Registry()
    )
    assert isinstance(channel, OutboundMetricChannel), "Incorrect channel type"


def test_outbound_metric_channel_from_settings():
    channel = OutboundMetricChannel.from_settings(
        settings=Channel(id="metrics/publisher", type=""), metric_queue=MetricQueue(), registry=Registry()
    )
    assert isinstance(channel, OutboundMetricChannel), "Incorrect channel type"


@pytest.mark.asyncio
async def test_outbound_metric_channel_send():
    queue = MetricQueue()
    registry = Registry()
    total_requests = MetricModel(
        kind=MetricsTypes.counter, name="total_requests", doc="Total requests", timestamp=0, values=0
    )
    channel = OutboundMetricChannel.from_settings(
        settings=Channel(
            id="metrics/publisher",
            type="",
        ),
        metric_queue=queue,
        registry=registry,
    )
    await channel.send(total_requests)

    metric = await queue.receive()
    assert metric == total_requests, "Incorrect metric (total_requests) sent/received"


@pytest.mark.asyncio
async def test_outbound_metric_channel_send_incorrect_metric_type():
    queue = MetricQueue()
    registry = Registry()
    total_requests = {
        "kind": MetricsTypes.counter,
        "name": "total_requests",
        "doc": "Total requests",
        "timestamp": 0,
        "values": 0,
    }
    channel = OutboundMetricChannel(id="metrics/publisher", metric_queue=queue, registry=registry)
    with pytest.raises(RuntimeError) as err:
        await channel.send(total_requests)
    assert (
        str(err.value) == "Incorrect metric type, founded: <class 'dict'>, expected: MetricModel"
    ), "Incorrect error message"
