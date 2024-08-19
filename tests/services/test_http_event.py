from sentinel.services.http_events import HTTPEventService


def test_http_event_service_init():
    http_event_service = HTTPEventService(endpoint_url="http://localhost", token="token")
    assert isinstance(http_event_service, HTTPEventService), "Incorrect HTTPEventService type"
