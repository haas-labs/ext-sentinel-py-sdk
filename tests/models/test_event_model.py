import time
from sentinel.models.event import Event, Blockchain


def test_event_id_generation():
    event1 = Event(
        did="TestDetector",
        type="text_event_type",
        severity=0.01,
        ts=int(time.time() * 1000),
        blockchain=Blockchain(network="ethereum", chain_id="1"),
    )
    assert isinstance(event1, Event), "Incorrect event type"

    event2 = Event(
        did="TestDetector",
        type="text_event_type",
        severity=0.01,
        ts=int(time.time() * 1000),
        blockchain=Blockchain(network="ethereum", chain_id="1"),
    )
    assert event1.eid != event2.eid, "Detected Event EID field value duplicates"
