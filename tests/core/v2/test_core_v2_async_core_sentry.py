import pathlib

import pytest
from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.models.channel import Channel
from sentinel.models.event import Blockchain, Event
from sentinel.models.sentry import Sentry
from sentinel.models.transaction import Transaction
from sentinel.utils.logger import Logger


def test_async_core_sentry_init():
    sentry = AsyncCoreSentry()
    assert isinstance(sentry, AsyncCoreSentry), "Incorrect async core sentry type"

    sentry.start()
    sentry.join()

    assert not sentry.is_alive(), "Sentry process is still alive"


def test_async_core_sentry_from_settings(tmpdir):
    class TestSentry(AsyncCoreSentry):
        async def on_init(self) -> None:
            await super().on_init()
            self.inputs.transactions.on_transaction = self.on_transaction

        async def on_transaction(self, transaction: Transaction) -> None:
            self.outputs.events.send(transaction)

    transactions_path = pathlib.Path("tests/core/v2/resources/data/transactions.jsonl")
    events_path = pathlib.Path(tmpdir)

    sentry_settings = Sentry(
        name="TestAsyncCoreSentry",
        type="TestSentry",
        parameters={"network": "ethereum"},
        inputs=[
            Channel(
                type="sentinel.channels.fs.transactions.InboundTransactionsChannel",
                id="local/fs/transactions",
                parameters={"path": transactions_path},
            )
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
    sentry = TestSentry.from_settings(settings=sentry_settings)
    assert isinstance(sentry, TestSentry), "Incorrect sentry type"

    sentry.init()
    assert isinstance(sentry.logger, Logger), "Incorrect logger type"
    assert sentry.inputs is not None, "Empty inputs list"
    assert sentry.outputs is not None, "Empty outputs list"
    assert sentry.inputs.transactions is not None, "Incorrect status of inbound transactions channel"
    assert sentry.outputs.events is not None, "Incorrect status of outbound events channel"


@pytest.mark.asyncio
async def test_async_core_sentry_run(tmpdir):
    class TestSentry(AsyncCoreSentry):
        async def on_init(self) -> None:
            await super().on_init()
            self.inputs.transactions.on_transaction = self.on_transaction

        async def on_transaction(self, transaction: Transaction) -> None:
            await self.outputs.events.send(
                Event(
                    did="TestSentry",
                    severity=0.1,
                    type="test_event_msg",
                    ts=0,
                    blockchain=Blockchain(network="test", chain_id="0"),
                )
            )

    transactions_path = pathlib.Path("tests/core/v2/resources/data/transactions.jsonl")
    events_path = pathlib.Path(tmpdir / "events.json")

    sentry_settings = Sentry(
        name="TestAsyncCoreSentry",
        type="TestSentry",
        parameters={"network": "ethereum"},
        inputs=[
            Channel(
                type="sentinel.channels.fs.transactions.InboundTransactionsChannel",
                id="local/fs/transactions",
                parameters={
                    "path": transactions_path,
                },
            )
        ],
        outputs=[
            Channel(
                type="sentinel.channels.fs.events.OutboundEventsChannel",
                id="local/fs/events",
                parameters={"path": events_path, "stop_after": 1},
            )
        ],
    )
    sentry = TestSentry.from_settings(settings=sentry_settings)
    sentry.init()

    await sentry.on_init()
    await sentry.processing()
