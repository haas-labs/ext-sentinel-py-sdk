"""
Detector Manifest

References
-------------
- https://extractor.hacken.dev/q/doc/#/Detector%20Schema%20Route/post_api_v1_schema

"""

from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field


class Severity(str, Enum):
    INFO = "INFO"  # 0
    LOW = "LOW"  # 0.15
    MEDIUM = "MEDIUM"  # 0.25
    HIGH = "HIGH"  # 0.5
    CRITICAL = "CRITICAL"  # 0.75


class NetworkTag(str, Enum):
    # Network groups
    EVM = "evm"
    ICP = "icp"
    STELLAR = "stellar"
    VECHAIN = "vechain"

    # EVM Networks
    ARBITRUM = "arbitrum"
    BSC = "bsc"
    BSC_TESTNET = "bsc_testnet"
    ETHEREUM = "ethereum"
    LINEA = "linea"
    OPTIMISM = "optimism"
    BASE = "base"
    GNOSIS = "gnosis"
    FANTOM = "fantom"
    POLYGON = "polygon"
    BLAST = "blast"
    ZKSYNC = "zksync"
    SCROLL = "scroll"
    AVALANCHE = "avalanche"

    # // test
    ANVIL = "anvil"


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    DELETED = "DELETED"


class FAQModel(BaseModel):
    name: str
    value: str


class BaseSchema(BaseModel): ...


class MetadataModel(BaseModel):
    name: str
    version: str
    description: str
    tags: List[NetworkTag] = Field(default_factory=list)
    faq: List[FAQModel] = Field(default_factory=list)
    status: Status


class ManifestAPIModel(MetadataModel):
    id: int
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    jsonschema: Dict = Field(default_factory=dict, alias="schema")