from typing import List

import httpx
from sentinel.models.event import Event

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class HTTPEventService:
    def __init__(self, endpoint_url: str, token: str) -> None:
        self._token = token
        self._endpoint_url = endpoint_url

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"

    def send(self, events: List[Event]) -> None:
        endpoint_url = self._endpoint + "/api/v1/event"
        query = {"events": events}

        with httpx.Client(verify=False) as httpx_client:
            response = httpx_client.post(url=endpoint_url, headers=self._headers, json=query)
            match response.status_code:
                case 200:
                    # self.logger.debug(f"{response}")
                    # The event sent successfully, check the number of accepted events
                    content = response.json()
                    if content.get("count", 0) != 1:
                        self.logger.error(
                            f"Publishing HTTP event failed, status code: {response.status_code}, "
                            + f"response: {content}, query: {query}"
                        )
                case _:
                    self.logger.error(
                        f"Publishing HTTP Event failed, status code: {response.status_code}, "
                        + f"response: {response.content}, query: {query}"
                    )
