import pytest
from sentinel.channels.kafka.events import OutboundEventsChannel as KafkaOutboundEventsChannel
from sentinel.core.v2.channel import SentryOutputs
from sentinel.models.channel import Channel

OUTPUTS = [
    Channel(
        id="kafka_events",
        type="sentinel.channels.kafka.events.OutboundEventsChannel",
        parameters={
            "bootstrap_servers": "localhost:9092",
            "topics": [
                "sentinel.events",
            ],
        },
    ),
    Channel(
        id="failed",
        type="sentinel.channels.ws.transaction",
    ),
]


def test_sentry_channel_outputs_success_import():
    outputs = SentryOutputs(ids=["kafka_events"], channels=OUTPUTS)
    assert isinstance(outputs, SentryOutputs), "Incorrect Sentry Inputs type"
    assert outputs.channels == ["events"], "Incorrect channel list"
    assert hasattr(outputs, "events"), "Missed event's channel"
    assert isinstance(outputs.events, KafkaOutboundEventsChannel), "Incorrect events channel type"
    assert outputs.events is not None, "Events channel shouldn't be None"


def test_sentry_channel_outputs_failed_import():
    with pytest.raises(RuntimeError):
        SentryOutputs(ids=["kafka_transactions"], channels=OUTPUTS)

    with pytest.raises(RuntimeError):
        SentryOutputs(ids=["failed"], channels=OUTPUTS)
