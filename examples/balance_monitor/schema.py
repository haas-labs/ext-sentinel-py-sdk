from pydantic import BaseModel, Field


class BalanceMonitorSchema(BaseModel):
    "Balance Monitor Schema"

    erc20_addr: str = Field(title="ERC20 Address", description="ERC20 Address")
    erc20_balance_threshold: int = Field(title="ERC20 Balance Threshold", description="ERC20 Balance Threshold")
    erc20_decimals: int = Field(title="ERC20 Decimals", description="ERC20 Decimals")
    balance_threshold: float = Field(title="Balance Threshold", description="Balance Threshold", ge=0.0, le=1.0)
    severity: float = Field(title="Severity", description="Severity")
    decimals: int = Field(title="Decimals", description="Decimals")

    @staticmethod
    def revision():
        return ("Test-Balance-Monitor", "0.1.0")
