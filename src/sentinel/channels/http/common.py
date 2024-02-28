import json
import httpx
import asyncio
import logging

from typing import Dict, Union

from pydantic import BaseModel
from sentinel.channels.common import OutboundChannel


logger = logging.getLogger(__name__)


DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE = 1000
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class OutboundHTTPChannel(OutboundChannel):
    """
    Outbound HTTP/REST Channel
    """

    def __init__(
        self,
        name: str,
        record_type: str,
        endpoint: str,
        token: str,
        chain_id: str,
        network: str,
        **kwargs,
    ) -> None:
        """
        Outbound HTTP/REST Channel Init
        """
        super().__init__(name, record_type, **kwargs)
        self._endpoint = endpoint
        self._token = token
        self._chain_id = chain_id
        self._network = network
        self.msg_queue = asyncio.Queue(maxsize=DEFAULT_INTERNAL_PRODUCER_QUEUE_SIZE)

    async def run(self) -> None:
        """
        Run Inbound HTTP/REST Channel Processing
        """
        logger.info(f"{self.name} -> Starting channel for publishing messages to events channel: {self.name}")
        endpoint_url = self._endpoint + "/api/v1/event/"

        while True:
            msg = await self.msg_queue.get()
            query = {"events": [msg]}

            print(msg)
            async with httpx.AsyncClient(verify=False) as httpx_async_client:
                response = await httpx_async_client.post(url=endpoint_url, headers=self._headers, json=query)

                print(response)
                if response.status_code != 200:
                    logger.error(
                        f"Message publishing error, status code: {response.status_code}, "
                        + f"response: {response.content}, query: {query}"
                    )

    async def send(self, msg: Union[Dict, BaseModel]) -> None:
        """
        Send message to in-process Queue
        """
        if isinstance(msg, Dict):
            msg = self.record_type(**msg)

        if isinstance(msg, self.record_type):
            self.msg_queue.put_nowait(msg.model_dump(exclude_none=True))
        else:
            raise RuntimeError(f"Unknown message type, type: {type(msg)}, " + "supported: Dict or pydantic.BaseModel")
