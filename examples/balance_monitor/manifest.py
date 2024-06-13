from pydantic import Field
from sentinel.manifest import BaseSchema, MetadataModel, Status


class Schema(BaseSchema):
    erc20_addr: str = Field(title="ERC20 Address", description="ERC20 Address")
    erc20_balance_threshold: int = Field(
        title="ERC20 Balance Threshold", description="ERC20 Balance Threshold", default=300000000000
    )
    erc20_decimals: int = Field(title="ERC20 Decimals", description="ERC20 Decimals", default=8)
    balance_threshold: float = Field(
        title="Balance Threshold", description="Balance Threshold", default=100000000000000000000.0000
    )
    severity: float = Field(title="Severity", description="Severity", ge=0.0, le=1.0)
    decimals: int = Field(title="Decimals", description="Decimals", default=18)


metadata = MetadataModel(
    name="Test-Balance-Monitor",
    version="0.1.1",
    status=Status.active,
    description="Test Balance Monitor Detector",
    faq=[
        {
            "name": "What is for?",
            "value": "Monitors Account/Contract balance (native token)",
        }
    ],
)
