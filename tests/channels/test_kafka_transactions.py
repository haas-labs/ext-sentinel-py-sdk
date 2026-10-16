import copy
import json
import pathlib
from types import SimpleNamespace

import pytest

from sentinel.channels.kafka.transactions import InboundTransactionsChannel, is_empty_block_placeholder
from sentinel.models.transaction import Transaction

RESOURCES = pathlib.Path(__file__).parent / "resources"

# Real record from the ADI tx topic: the trunk ingest publishes it for an empty block (transaction_count == 0)
EMPTY_BLOCK_PLACEHOLDER = json.loads((RESOURCES / "adi_empty_block_placeholder.json").read_text())
# Real regular transaction from the same topic
TRANSACTION = json.loads((RESOURCES / "adi_transaction.json").read_text())


def message(value, offset: int = 0) -> SimpleNamespace:
    return SimpleNamespace(value=value, offset=offset)


@pytest.fixture
def channel():
    channel = InboundTransactionsChannel(
        name="transactions",
        sentry_name="test_sentry",
        sentry_hash="test_hash",
        topics=["adi.mainnet.tx"],
        bootstrap_servers="localhost:9092",
    )
    channel.received = []

    async def on_transaction(transaction: Transaction) -> None:
        channel.received.append(transaction)

    channel.on_transaction = on_transaction
    return channel


def test_is_empty_block_placeholder():
    assert is_empty_block_placeholder(EMPTY_BLOCK_PLACEHOLDER)
    assert not is_empty_block_placeholder(TRANSACTION)
    assert not is_empty_block_placeholder(None)

    # empty hash in a non-empty block is not the trunk placeholder
    record = copy.deepcopy(EMPTY_BLOCK_PLACEHOLDER)
    record["block"]["transaction_count"] = 1
    assert not is_empty_block_placeholder(record)


@pytest.mark.asyncio
async def test_kafka_transactions_skip_empty_block_placeholder(channel):
    await channel.on_message(message(EMPTY_BLOCK_PLACEHOLDER, offset=46941))
    assert channel.received == [], "Empty block placeholder must not reach the sentry"


@pytest.mark.asyncio
async def test_kafka_transactions_normal_transaction(channel):
    await channel.on_message(message(TRANSACTION))
    assert len(channel.received) == 1
    assert isinstance(channel.received[0], Transaction)
    assert channel.received[0].hash == TRANSACTION["hash"]


@pytest.mark.asyncio
async def test_kafka_transactions_invalid_transaction_still_raises(channel):
    record = copy.deepcopy(TRANSACTION)
    record.pop("gas_price")
    with pytest.raises(RuntimeError, match="gas_price"):
        await channel.on_message(message(record))
    assert channel.received == []
