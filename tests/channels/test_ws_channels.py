from sentinel.channels.ws.common import WebsocketChannel, InboundWebsocketChannel


def test_ws_channel_init():
    """
    Test Websocker Channel Init
    """
    channel = WebsocketChannel(
        name="test-ws-channel", record_type="sentinel.models.transaction.Transaction", kwargs={}
    )
    assert isinstance(channel, WebsocketChannel), "Incorrect websocker channel type"


def test_inbound_ws_channel_init():
    """
    Test Inbound Websocker Channel Init
    """
    channel = InboundWebsocketChannel(
        name="test-ws-channel", record_type="sentinel.models.transaction.Transaction", kwargs={}
    )
    assert isinstance(channel, InboundWebsocketChannel), "Incorrect inbound websocker channel type"

