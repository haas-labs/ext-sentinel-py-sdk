from typing import List

from pydantic import Field
from typing_extensions import TypedDict

from sentinel.manifest import BaseSchema, MetadataModel, NetworkTag, Status, Tag


class TokenThreshold(TypedDict, total=False):
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
    decimals: int = Field(title="Decimals", description="Decimals", default=18)
    tokens: List[str] = Field(title="Tokens", description="Monitored Tokens", default=["0x0001", "0x0002", "0x0004"])
    token_thresholds: List[TokenThreshold] = Field(
        title="Token thresholds",
        description="Options to specify thresholds per token",
        default=[TokenThreshold(token="0x001", threshold=100), TokenThreshold(token="0x002", threshold=200)],
    )


metadata = MetadataModel(
    name="Test-Balance-Monitor",
    version="0.1.11",
    status=Status.ACTIVE,
    description="Test Balance Monitor Detector",
    tags=[
        Tag.FINANCIAL,
    ],
    network_tags=[
        NetworkTag.EVM,
    ],
    faq=[
        {
            "name": "What is for?",
            "value": "Monitors Account/Contract balance (native token)",
        }
    ],
    ui_schema={
        "ui:order": [
            "erc20_addr",
            "erc20_balance_threshold",
            "erc20_decimals",
            "balance_threshold",
            "decimals",
            "tokens",
            "token_thresholds",
            "severity",
        ]
    },
)
