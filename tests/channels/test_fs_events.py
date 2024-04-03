import pathlib
from sentinel.channels.fs.events import OutboundEventsChannel


def test_fs_channel_events_init(tmpdir):
    events = OutboundEventsChannel(path=pathlib.Path(tmpdir / "events.json"))
    assert isinstance(events, OutboundEventsChannel), "Incorrect events channel type"
