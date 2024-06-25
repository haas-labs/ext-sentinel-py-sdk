from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DELETED = "DELETED"


class Contract(BaseModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    project_id: int = Field(alias="projectId")
    tenant_id: int = Field(alias="tenantId")
    chain_uid: str = Field(alias="chainUid")
    proxy_address: str | None = Field(alias="proxyAddress")
    address: str
    name: str


class ConfigSchema(BaseModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    status: Status
    name: str
    version: str
    jsonschema: Dict = Field(alias="schema", default_factory=dict)


class Target(BaseModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    status: Status
    name: str
    source: str
    contract: Contract
    tags: List[str] = Field(default_factory=list)
    config_schema: ConfigSchema = Field(alias="schema")

    # Configuration based on published scheme for detector
    # TODO need to make data validation before use in a detector
    config: Dict = Field(default_factory=Dict)
