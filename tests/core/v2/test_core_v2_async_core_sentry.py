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


def test_sentry_async_core_from_settings():
    sentry_settings = Sentry(
        name="TestAsyncCoreSentry",
        type="sentinel.core.v2.sentry.AsyncCoreSentry",
        parameters={"network": "ethereum"},
        inputs=[
            Channel(type="sentinel.channels.fs.transactions.InboundTransactionsChannel", id="local/fs/transactions")
        ],
        outputs=[Channel(type="sentinel.channels.fs.events.OutboundEventsChannel", id="local/fs/events")],
        databases=[],
    )
    sentry = AsyncCoreSentry.from_settings(settings=sentry_settings)
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect sntry type"

    sentry.init()
    assert isinstance(sentry.logger, Logger), "Incorrect logger type"

    assert False
