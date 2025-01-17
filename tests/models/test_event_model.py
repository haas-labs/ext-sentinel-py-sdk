import time

from sentinel.models.event import Blockchain, Event, get_hash_id


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


def test_get_hash_id():
    event_field_values = (
        "name:TestDetector"
        + "type:text_event_type"
        + "severity:0.01"
        + "ts:1737103230654"
        + "network:ethereum"
        + "chain_id:1"
    )
    assert get_hash_id(event_field_values) == "1cf067c99431615cf9be46f45b19c1b414a560067b9a00a067a50bcd70155055"
