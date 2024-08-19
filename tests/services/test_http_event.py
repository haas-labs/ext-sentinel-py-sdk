import time

from pytest_httpx import HTTPXMock
from sentinel.models.event import Blockchain, Event
from sentinel.services.http_event import HTTPEventService


def test_http_event_service_init():
    http_event_service = HTTPEventService(endpoint_url="http://localhost", token="token")
    assert isinstance(http_event_service, HTTPEventService), "Incorrect HTTPEventService type"


def test_http_event_service_send_event(httpx_mock: HTTPXMock):
    event_time = int(time.time())
    eid = "3861846de2fe474aa04b10d15ec6fd64"
    httpx_mock.add_response(
        match_json={
            "events": [
                {
                    "did": "TestDetector",
                    "eid": eid,
                    "sid": "ext:ad",
                    "category": "EVENT",
                    "type": "test_event",
                    "severity": 0.1,
                    "ts": event_time,
                    "blockchain": {"network": "ethereum", "chain_id": "1"},
                    "metadata": {},
                }
            ]
        },
        json={"count": 1},
    )

    http_event_service = HTTPEventService(endpoint_url="http://localhost", token="token")
    event = Event(
        did="TestDetector",
        eid=eid,
        type="test_event",
        severity=0.1,
        ts=event_time,
        blockchain=Blockchain(network="ethereum", chain_id="1"),
    )
    http_event_service.send(event=event)
