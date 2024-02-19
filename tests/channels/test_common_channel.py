from sentinel.channels.common import Channel


def test_common_channel_init():
    """
    Test Common Channel Init
    """
    channel = Channel(name="test-channel", record_type="sentinel.models.transaction.Transaction", kwargs={})
    assert isinstance(channel, Channel), "Incorrect common channel type"
