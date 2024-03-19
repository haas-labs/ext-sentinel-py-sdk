from sentinel.models.channel import Channel
from sentinel.sentry.channel import SentryInputs
from sentinel.channels.fs.transactions import InboundTransactionsChannel as FSInboundTransactionsChannel
from sentinel.channels.kafka.transactions import InboundTransactionsChannel as KafkaInboundTransactionsChannel
from sentinel.channels.ws.transactions import InboundTransactionChannel as WSInboundTransactionChannel

INPUTS = [
    Channel(
        id="kafka_transactions",
        type="sentinel.channels.kafka.transactions.InboundTransactionsChannel",
        parameters={
            "bootstrap_servers": "localhost:9092",
            "group_id": "sentinel.transactions",
            "auto_offset_reset": "latest",
            "topics": [
                "ethereum.mainnet.tx",
            ],
        },
    ),
    Channel(
        id="fs_transactions",
        type="sentinel.channels.fs.transactions.InboundTransactionsChannel",
        parameters={
            "path": "./data/transactions.json",
        },
    ),
    Channel(
        id="ws_transactions",
        type="sentinel.channels.ws.transactions.InboundTransactionChannel",
        parameters={
            "server_uri": "ws://localhost:9300",
            # server_uri: {{ env['ETH_WS_URL'] }}
        },
    ),
    Channel(
        id="failed",
        type="sentinel.channels.ws.transaction",
    ),
]


def test_sentry_channel_inputs_success_import():
    inputs = SentryInputs(ids=["kafka_transactions"], channels=INPUTS)
    assert isinstance(inputs, SentryInputs), "Incorrect Sentry Inputs type"
    assert inputs.channels == ["transactions"], "Incorrect channel list"
    assert hasattr(inputs, "transactions"), "Missed transaction's channel"
    assert isinstance(inputs.transactions, KafkaInboundTransactionsChannel), "Incorrect transaction channel type"

    inputs = SentryInputs(ids=["fs_transactions"], channels=INPUTS)
    assert isinstance(inputs, SentryInputs), "Incorrect Sentry Inputs type"
    assert inputs.channels == ["transactions"], "Incorrect channel list"
    assert hasattr(inputs, "transactions"), "Missed transaction's channel"
    assert isinstance(inputs.transactions, FSInboundTransactionsChannel), "Incorrect transaction channel type"

    inputs = SentryInputs(ids=["ws_transactions"], channels=INPUTS)
    assert isinstance(inputs, SentryInputs), "Incorrect Sentry Inputs type"
    assert inputs.channels == ["transactions"], "Incorrect channel list"
    assert hasattr(inputs, "transactions"), "Missed transaction's channel"
    assert isinstance(inputs.transactions, WSInboundTransactionChannel), "Incorrect transaction channel type"


def test_sentry_channel_inputs_failed_import():
    inputs = SentryInputs(ids=["kafka_events"], channels=INPUTS)
    assert isinstance(inputs, SentryInputs), "Incorrect Sentry Inputs type"
    assert inputs.channels == [], "Imported incorrect channel(-s)"

    inputs = SentryInputs(ids=["failed"], channels=INPUTS)
    assert isinstance(inputs, SentryInputs), "Incorrect Sentry Inputs type"
    assert inputs.channels == [], "Imported incorrect channel(-s)"
