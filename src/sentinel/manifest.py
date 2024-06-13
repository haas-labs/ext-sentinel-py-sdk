"""
Detector Manifest

References
-------------
- https://extractor.hacken.dev/q/doc/#/Detector%20Schema%20Route/post_api_v1_schema

"""

from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field


class Status(str, Enum):
    active = "ACTIVE"
    disabled = "DISABLED"
    deleted = "DELETED"


class FAQModel(BaseModel):
    name: str
    value: str


class BaseSchema(BaseModel): ...


class MetadataModel(BaseModel):
    name: str
    version: str
    description: str
    tags: List[str] = Field(default_factory=list)
    faq: List[FAQModel] = Field(default_factory=list)
    status: Status


class ManifestAPIModel(MetadataModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    jsonschema: Dict = Field(default_factory=dict, alias="schema")
