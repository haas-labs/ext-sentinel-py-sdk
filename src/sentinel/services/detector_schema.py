import os
from enum import Enum
from typing import Dict, Iterator

import httpx
from pydantic import BaseModel, Field
from sentinel.utils.logger import get_logger

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class SchemaStatus(str, Enum):
    active = "ACTIVE"
    disabled = "DISABLED"
    deleted = "DELETED"


class SchemaModel(BaseModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    status: SchemaStatus
    name: str
    version: str
    jsonschema: Dict = Field(default_factory=dict, alias="schema")


class DetectorSchemaAPI:
    def __init__(self) -> None:
        """
        Service Account Token Init
        """
        self._endpoint_url = os.environ.get("EXTRACTOR_API_ENDPOINT")
        self._token = os.environ.get("EXT_API_TOKEN")

        self._headers = DEFAULT_HEADERS.copy()
        self._headers["Authorization"] = f"Bearer {self._token}"
        self.logger = get_logger("DetectorSchemaAPI")

    def change(self, schema_id: int, name: str = None, status: SchemaStatus = None) -> None:
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
                            "status": status,
                            "status code": response.status_code,
                            "response": response.text,
                        }
                    )
                )

    def register(self, name: str, version: str, schema: str) -> None:
        endpoint = self._endpoint_url + "/api/v1/schema"
        data = {
            "status": SchemaStatus.active.value,
            "name": name,
            "version": version,
            "schema": schema,
        }
        response = httpx.post(url=endpoint, headers=self._headers, json=data, verify=False)
        match response.status_code:
            case 200:
                self.logger.info("The schema registered succesfully")
            case _:
                self.logger.error(
                    "Registering schema failed, {}".format(
                        {
                            "name": name,
                            "version": version,
                            "status code": response.status_code,
                            "response": response.text,
                        }
                    )
                )

    def get(self, schema_id: int = None, name: str = None, version: str = None) -> Iterator[SchemaModel]:
        endpoint = self._endpoint_url + "/api/v1/schema/search"

        query = {}
        if schema_id is not None:
            query = {"where": f"id = {schema_id}"}
        elif name is not None and version is not None:
            query = {"where": f"name = '{name}' and version = '{version}'"}
        elif name is not None and version is None:
            query = {"where": f"name = '{name}'"}

        response = httpx.post(url=endpoint, headers=self._headers, json=query, verify=False)
        match response.status_code:
            case 200:
                content = response.json()
                for schema in content.get("data", []):
                    yield SchemaModel(**schema)
            case _:
                self.logger.error(
                    f"Getting detector schema failed, status code: {response.status_code}, query: {query}"
                )

    def show(self, path: str) -> None: ...

    def validate(self, path: str) -> None: ...
