import pathlib

from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.models.channel import Channel
from sentinel.models.sentry import Sentry
from sentinel.utils.logger import Logger


def test_sentry_async_core_init():
    sentry = AsyncCoreSentry()
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect async core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"


def test_sentry_async_core_from_settings(tmpdir):
    events_path = pathlib.Path(tmpdir)
    sentry_settings = Sentry(
        name="TestAsyncCoreSentry",
        type="sentinel.core.v2.sentry.AsyncCoreSentry",
        parameters={"network": "ethereum"},
        inputs=[
            Channel(type="sentinel.channels.fs.transactions.InboundTransactionsChannel", id="local/fs/transactions")
        ],
        outputs=[
            Channel(
                type="sentinel.channels.fs.events.OutboundEventsChannel",
                id="local/fs/events",
                parameters={"path": events_path},
            )
        ],
        databases=[],
    )
    sentry = AsyncCoreSentry.from_settings(settings=sentry_settings)
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect sntry type"

    sentry.init()
    assert isinstance(sentry.logger, Logger), "Incorrect logger type"
    assert sentry.inputs is not None, "Empty inputs list"
    assert sentry.outputs is not None, "Empty outputs list"
    assert sentry.inputs.transactions is not None, "Incorrect status of inbound transactions channel"
    assert sentry.outputs.events is not None, "Incorrect status of outbound events channel"
