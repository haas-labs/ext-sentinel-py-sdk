"""
Detector Manifest

References
-------------
- https://extractor.hacken.dev/q/doc/#/Detector%20Schema%20Route/post_api_v1_schema

"""

from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field


class Severity(float, Enum):
    AUTO = -1
    INFO = 0
    LOW = 0.15
    MEDIUM = 0.25
    HIGH = 0.5
    CRITICAL = 0.75


class Tag(str, Enum):
    SECURITY = "SECURITY"
    COMPLIANCE = "COMPLIANCE"
    FINANCIAL = "FINANCIAL"


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


class BaseSchema(BaseModel):
    severity: float = Field(title="Severity", description="Severity", default=-1.0)


class MetadataModel(BaseModel):
    name: str
    version: str
    description: str
    tags: List[str] = Field(default_factory=list)
    network_tags: List[str] = Field(default_factory=list)
    faq: List[FAQModel] = Field(default_factory=list)
    status: Status


class ManifestAPIModel(MetadataModel):
    id: int
    author: str | None
    icon: str | None
    status: Status
    version: str
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")
    json_schema: Dict = Field(default_factory=dict, alias="schema")
    ui_schema: Dict = Field(default_factory=dict, alias="uiSchena")
