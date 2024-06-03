import pathlib

import pytest
from sentinel.channels.fs.events import OutboundEventsChannel
from sentinel.core.v2.channel import Channel
from sentinel.models.event import Blockchain, Event


def test_fs_channel_events_init(tmpdir):
    channel = OutboundEventsChannel(name=OutboundEventsChannel.name, path=pathlib.Path(tmpdir / "events.json"))
    assert isinstance(channel, OutboundEventsChannel), "Incorrect events channel type"
    assert channel.name == OutboundEventsChannel.name, "Incorrect events channel name"


def test_fs_channel_events_init_from_settings(tmpdir):
    channel = OutboundEventsChannel.from_settings(
        settings=Channel(
            name=OutboundEventsChannel.name,
            type="",
            parameters={
                "path": pathlib.Path(tmpdir / "events.json"),
            },
        )
    )
    assert isinstance(channel, OutboundEventsChannel), "Incorrect events channel type"
    assert channel.name == OutboundEventsChannel.name, "Incorrect events channel name"


@pytest.mark.asyncio
async def test_fs_channel_events_run(tmpdir):
    channel = OutboundEventsChannel(
        name=OutboundEventsChannel.name, path=pathlib.Path(tmpdir / "events.json"), stop_after=1
    )
    await channel.send(
        Event(
            did="TestOutboundEventsChannel",
            type="test_msg",
            severity=0.1,
            ts=0,
            blockchain=Blockchain(network="ethereum", chain_id="1"),
        )
    )
    await channel.run()
