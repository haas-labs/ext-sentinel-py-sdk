from sentinel.channels.common import Channel, InboundChannel, OutboundChannel


def test_common_channel_init():
    """
    Test Common Channel Init
    """
    channel = Channel(name="test-channel", record_type="sentinel.models.transaction.Transaction", kwargs={})
    assert isinstance(channel, Channel), "Incorrect common channel type"


def test_inbound_channel_init():
    """
    Test Inbound Channel Init
    """
    channel = InboundChannel(
        name="test-inbound-channel", record_type="sentinel.models.transaction.Transaction", kwargs={}
    )
    assert isinstance(channel, InboundChannel), "Incorrect inbound channel type"

def test_outbound_channel_init():
    """
    Test Outbound Channel Init
    """
    channel = OutboundChannel(
        name="test-outbound-channel", record_type="sentinel.models.transaction.Transaction", kwargs={}
    )
    assert isinstance(channel, OutboundChannel), "Incorrect outbound channel type"
