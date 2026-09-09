import asyncio
import json

import httpx
import pytest

from sentinel.channels.http.webhook import OutboundWebhookChannel
from sentinel.models.event import Blockchain, Event


def _event(eid="e1"):
    return Event(did="D", eid=eid, type="t", severity=0.5, ts=1, blockchain=Blockchain(network="canton", chain_id="canton"), metadata={"party_hash": "abc"})


def _channel(handler, **kw):
    ch = OutboundWebhookChannel(name="webhook", url="http://receiver/hook", token="tok", backoff_seconds=0, **kw)
    return ch, httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.mark.asyncio
async def test_delivers_with_bearer_and_event_id():
    seen = []
    def handler(request):
        seen.append((request.headers.get("Authorization"), request.headers.get("X-Event-Id"), json.loads(request.content)))
        return httpx.Response(202)
    ch, client = _channel(handler)
    assert await ch.deliver(client, _event("e42").model_dump(exclude_none=True))
    auth, eid, body = seen[0]
    assert auth == "Bearer tok" and eid == "e42" and body["metadata"]["party_hash"] == "abc" and ch.delivered == 1


@pytest.mark.asyncio
async def test_retries_on_5xx_then_succeeds():
    calls = []
    def handler(request):
        calls.append(1)
        return httpx.Response(503) if len(calls) < 3 else httpx.Response(200)
    ch, client = _channel(handler, max_attempts=5)
    assert await ch.deliver(client, _event().model_dump(exclude_none=True)) and len(calls) == 3


@pytest.mark.asyncio
async def test_drops_on_4xx_without_retrying():
    calls = []
    def handler(request):
        calls.append(1)
        return httpx.Response(400, text="bad")
    ch, client = _channel(handler, max_attempts=5)
    assert not await ch.deliver(client, _event().model_dump(exclude_none=True)) and len(calls) == 1 and ch.dropped == 1


@pytest.mark.asyncio
async def test_gives_up_after_max_attempts_when_unreachable():
    def handler(request):
        raise httpx.ConnectError("down")
    ch, client = _channel(handler, max_attempts=3)
    assert not await ch.deliver(client, _event().model_dump(exclude_none=True)) and ch.dropped == 1


@pytest.mark.asyncio
async def test_send_queues_events_only():
    ch, _ = _channel(lambda r: httpx.Response(200))
    await ch.send(_event("q1"))
    assert ch.queue.qsize() == 1 and ch.queue.get_nowait()["eid"] == "q1"
    with pytest.raises(TypeError):
        await ch.send("not an event")
