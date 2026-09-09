"""
Outbound webhook: POST every Event, one per request, to any URL a client configures (its SIEM, a
compliance vendor, the Extractor's own intake through a proxy). Built for the Canton
participant-local deployment, where the alert has to cross the client's boundary by HTTP and is
the only thing that crosses it.

Delivery: in-process queue, retries with exponential backoff on connection errors and 5xx,
idempotency key in the X-Event-Id header (the Event's eid), so a receiver can drop repeats. A 4xx
other than 408 / 429 is logged and dropped: the payload will not become valid by retrying.
"""

import asyncio
from typing import Dict, Optional, Union

import httpx
from pydantic import BaseModel

from sentinel.channels.common import OutboundChannel
from sentinel.core.v2.channel import ChannelModel
from sentinel.models.event import Event

DEFAULT_QUEUE_SIZE = 10000
RETRYABLE = {408, 425, 429, 500, 502, 503, 504}


class OutboundWebhookChannel(OutboundChannel):
    name = "webhook"

    def __init__(
        self,
        name: str,
        url: str,
        token: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        max_attempts: int = 8,
        backoff_seconds: float = 1.0,
        timeout_seconds: float = 10.0,
        record_type: str = "sentinel.models.event.Event",
        **kwargs,
    ) -> None:
        super().__init__(name=name, record_type=record_type, **kwargs)
        if not url:
            raise ValueError("The webhook 'url' parameter is missing")
        self.url = url
        self.max_attempts = max_attempts
        self.backoff = backoff_seconds
        self.timeout = timeout_seconds
        self.headers = {"Content-Type": "application/json", **(headers or {})}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=DEFAULT_QUEUE_SIZE)
        self.delivered = 0
        self.dropped = 0

    @classmethod
    def from_settings(cls, settings: ChannelModel, **kwargs):
        kwargs.update(settings.parameters)
        return cls(name=settings.name, **kwargs)

    async def run(self) -> None:
        self.logger.info(f"{self.name} -> delivering events to webhook {self.url}")
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            while True:
                payload = await self.queue.get()
                await self.deliver(client, payload)

    async def deliver(self, client: httpx.AsyncClient, payload: Dict) -> bool:
        headers = {**self.headers, "X-Event-Id": str(payload.get("eid", ""))}
        for attempt in range(1, self.max_attempts + 1):
            try:
                response = await client.post(self.url, headers=headers, json=payload)
                if response.status_code < 300:
                    self.delivered += 1
                    return True
                if response.status_code not in RETRYABLE:
                    self.logger.error(f"{self.name} -> webhook rejected event {payload.get('eid')}: {response.status_code} {response.text[:200]}")
                    self.dropped += 1
                    return False
                self.logger.warning(f"{self.name} -> webhook {response.status_code} on attempt {attempt}, retrying")
            except httpx.HTTPError as err:
                self.logger.warning(f"{self.name} -> webhook unreachable on attempt {attempt}: {err}")
            await asyncio.sleep(self.backoff * (2 ** (attempt - 1)))
        self.logger.error(f"{self.name} -> giving up on event {payload.get('eid')} after {self.max_attempts} attempts")
        self.dropped += 1
        return False

    async def send(self, msg: Union[Dict, BaseModel]) -> None:
        if isinstance(msg, dict):
            msg = self.record_type(**msg)
        if not isinstance(msg, Event):
            raise TypeError(f"{self.name} -> unsupported message type: {type(msg)}")
        await self.queue.put(msg.model_dump(exclude_none=True))
