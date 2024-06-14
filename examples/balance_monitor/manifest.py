from typing import List

from pydantic import Field
from sentinel.manifest import BaseSchema, MetadataModel, NetworkTag, Severity, Status
from typing_extensions import TypedDict


class TokenThresholds(TypedDict, total=False):
    token: str
    threshold: int


class Schema(BaseSchema):
    erc20_addr: str = Field(title="ERC20 Address", description="ERC20 Address")
    erc20_balance_threshold: int = Field(
        title="ERC20 Balance Threshold", description="ERC20 Balance Threshold", default=300000000000
    )
    erc20_decimals: int = Field(title="ERC20 Decimals", description="ERC20 Decimals", default=8)
    balance_threshold: float = Field(
        title="Balance Threshold", description="Balance Threshold", default=100000000000000000000.0000
    )
    severity: Severity = Field(title="Severity", description="Severity", default=Severity.INFO)
    decimals: int = Field(title="Decimals", description="Decimals", default=18)
    tokens: List[str] = Field(title="Tokens", description="Monitored Tokens", default=["0x0001", "0x0002", "0x0004"])
    token_thresholds: List[TokenThresholds] = Field(
        title="Token thresholds", description="Options to specify thresholds per token", default_factory=list
    )


metadata = MetadataModel(
    name="Test-Balance-Monitor",
    version="0.1.8",
    status=Status.ACTIVE,
    description="Test Balance Monitor Detector",
    tags=[
        NetworkTag.EVM,
    ],
    faq=[
        {
            "name": "What is for?",
            "value": "Monitors Account/Contract balance (native token)",
        }
    ],
)
