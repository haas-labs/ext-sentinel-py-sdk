from sentinel.channels.metric.core import OutboundMetricChannel
from sentinel.core.v2.channel import Channel
from sentinel.metrics.registry import Registry


def test_outbound_metric_channel_init():
    channel = OutboundMetricChannel(id="metrics/publisher", name="metrics", registry=Registry())
    assert isinstance(channel, OutboundMetricChannel), "Incorrect channel type"


def test_outbound_metric_channel_from_settings():
    channel = OutboundMetricChannel.from_settings(
        settings=Channel(id="metrics/publisher", type=""), registry=Registry()
    )
    assert isinstance(channel, OutboundMetricChannel), "Incorrect channel type"
