import os
from typing import Iterator

import httpx

from sentinel.manifest import ManifestAPIModel, MetadataModel, Status
from sentinel.utils.logger import get_logger

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class ManifestAPI:
    def __init__(self) -> None:
        self._endpoint_url = os.environ.get("EXTRACTOR_API_ENDPOINT")
        if not self._endpoint_url:
            raise RuntimeError("Environment variable EXTRACTOR_API_ENDPOINT must be configured for Manifest API use")

        self._token = os.environ.get("EXT_API_TOKEN")
        if not self._token:
            raise RuntimeError("Environment variable EXT_API_TOKEN must be configured for Manifest API use")

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"
        self.logger = get_logger("ManifestAPI")

    def change(self, schema_id: int, name: str = None, status: Status = None) -> None:
        endpoint = self._endpoint_url + f"/api/v1/schema/{schema_id}"
        data = {}
        if name is not None:
            data["name"] = name
        if status is not None:
            data["status"] = status.value
        response = httpx.put(url=endpoint, headers=self._headers, json=data, verify=False)
        match response.status_code:
            case 200:
                self.logger.info("The schema updated succesfully")
            case _:
                self.logger.error(
                    "The schema update failed, {}".format(
                        {
                            "name": name,
                            "status": status.value,
                            "status code": response.status_code,
                            "response": response.text,
                        }
                    )
                )

    def register(self, metadata: MetadataModel, schema: str) -> None:
        endpoint = self._endpoint_url + "/api/v1/schema"
        data = {
            "name": metadata.name,
            "version": metadata.version,
            "author": metadata.author,
            "status": metadata.status.value,
            "description": metadata.description,
            "tags": metadata.tags,
            "networkTags": metadata.network_tags,
            "schema": schema,
            "faq": [faq.model_dump() for faq in metadata.faq],
            "uiSchema": metadata.ui_schema,
        }
        response = httpx.post(url=endpoint, headers=self._headers, json=data, verify=False)
        match response.status_code:
            case 200:
                self.logger.info("The schema registered succesfully")
            case _:
                self.logger.error(
                    " ".join(
                        [
                            f"Registering schema failed, manifest: {data},",
                            f"status code: {response.status_code},",
                            f"response: {response.text}",
                        ]
                    )
                )

    def get(
        self, schema_id: int = None, name: str = None, version: str = None, status: Status = None
    ) -> Iterator[ManifestAPIModel]:
        endpoint = self._endpoint_url + "/api/v1/schema/search"

        query = {
            "size": 100,
        }
        if schema_id is not None:
            query.update({"where": f"id = {schema_id}"})

        params = []
        if name is not None:
            params.append(("name", name))
        if version is not None:
            params.append(("version", version))
        if status is not None:
            params.append(("status", status.value))

        if len(params) > 0:
            query_str = " and ".join([f"{kv[0]}='{kv[1]}'" for kv in params])
            query["where"] = query_str

        try:
            response = httpx.post(url=endpoint, headers=self._headers, json=query, verify=False)
            match response.status_code:
                case 200:
                    content = response.json()
                    for manifest_data in content.get("data", []):
                        manifest = ManifestAPIModel(**manifest_data)
                        yield manifest
                case _:
                    self.logger.error(
                        "Getting detector schema failed, {}".format(
                            {"status code": response.status_code, "query": query, "response": response.text}
                        )
                    )
        except httpx.ConnectError as err:
            self.logger.error(f"Connection error: {err}")

    def show(self, path: str) -> None: ...

    def validate(self, path: str) -> None: ...
