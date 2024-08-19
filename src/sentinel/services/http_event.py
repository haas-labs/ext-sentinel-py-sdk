import httpx
from sentinel.models.event import Event
from sentinel.utils.logger import get_logger

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class HTTPEventService:
    def __init__(self, endpoint_url: str, token: str) -> None:
        self._token = token
        self._endpoint_url = endpoint_url + "/api/v1/event"

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"

        self.logger = get_logger(__name__)

    def send(self, event: Event) -> None:
        assert isinstance(event, Event), "Incorrect events type, expected list or tuple"

        query = {"events": [event.model_dump(exclude_none=True)]}
        with httpx.Client(verify=False) as httpx_client:
            response = httpx_client.post(
                url=self._endpoint_url,
                headers=self._headers,
                json=query,
            )
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
