import pathlib
from sentinel.channels.fs.events import OutboundEventsChannel


def test_fs_channel_events_init(tmpdir):
    channel = OutboundEventsChannel(name=OutboundEventsChannel.name, path=pathlib.Path(tmpdir / "events.json"))
    assert isinstance(channel, OutboundEventsChannel), "Incorrect events channel type"
    assert channel.name == OutboundEventsChannel.name, "Incorrect events channel name"
