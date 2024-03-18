from sentinel.sentry.channel import SentryOutputs
from sentinel.channels.kafka.events import OutboundEventsChannel as KafkaOutboundEventsChannel

OUTPUT_SETTINGS = {
    "outputs": [
        {
            "alias": "kafka_events",
            "type": "sentinel.channels.kafka.events.OutboundEventsChannel",
            "parameters": {
                "bootstrap_servers": "localhost:9092",
                "group_id": "sentinel.events",
                "topics": [
                    "sentinel.events",
                ],
            },
        },
    ]
}


def test_sentry_channel_outputs_success_import():
    outputs = SentryOutputs(aliases=["kafka_events"], settings=OUTPUT_SETTINGS)
    assert isinstance(outputs, SentryOutputs), "Incorrect Sentry Inputs type"
    assert hasattr(outputs, "events"), "Missed event's channel"
    assert isinstance(outputs.events, KafkaOutboundEventsChannel), "Incorrect events channel type"


def test_sentry_channel_outputs_failed_import():
    outputs = SentryOutputs(aliases=["kafka_events"], settings=OUTPUT_SETTINGS)
    assert isinstance(outputs, SentryOutputs), "Incorrect Sentry Outputs type"
    assert outputs.channels == [], "Imported incorrect channel(-s)"

    outputs = SentryOutputs(aliases=["failed"], settings=OUTPUT_SETTINGS)
    assert isinstance(outputs, SentryOutputs), "Incorrect Sentry Outputs type"
    assert outputs.channels == [], "Imported incorrect channel(-s)"
