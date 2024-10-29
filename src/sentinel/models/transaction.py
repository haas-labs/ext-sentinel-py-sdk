from typing import List, Optional

from pydantic import AliasChoices, BaseModel, Field


class Block(BaseModel):
    """
    EVM Based Transaction Block
    """

    hash: str
    number: int
    timestamp: int
    parent_hash: str
    nonce: str
    sha3_uncles: str
    logs_bloom: str
    transactions_root: str
    state_root: str
    receipts_root: str
    miner: str
    difficulty: int
    total_difficulty: Optional[int] = None
    size: int
    extra_data: str
    gas_limit: int
    gas_used: int
    base_fee_per_gas: Optional[int] = None
    transaction_count: int


class LogEntry(BaseModel):
    """
    Log Entry
    """

    index: int
    address: str
    data: str
    topics: List[str] = Field(default_factory=list)


class Transaction(BaseModel):
    """
    EVM based Transaction
    """

    hash: str
    nonce: int
    block: Block
    transaction_index: int
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    value: int
    gas: int
    gas_price: int
    gas_used: int = Field(validation_alias=AliasChoices("receipt_gas_used", "gas_used"))
    effective_gas_price: Optional[int] = Field(
        validation_alias=AliasChoices("receipt_effective_gas_price", "effective_gas_price"), default=None
    )
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    cumulative_gas_used: int = Field(
        validation_alias=AliasChoices("receipt_cumulative_gas_used", "cumulative_gas_used")
    )
    input: str
    contract_address: Optional[str] = Field(
        validation_alias=AliasChoices("receipt_contract_address", "contract_address"), default=None
    )
    root: Optional[str] = Field(validation_alias=AliasChoices("receipt_root", "root"))
    status: int = Field(validation_alias=AliasChoices("receipt_status", "status"))
    transaction_type: Optional[int] = None
    logs: List[LogEntry]
    attack_probablity: float = 0.0

    # TODO remove outdated fields after tests fix
    # type: Optional[str] = None
    # item_id: Optional[str] = None
    # item_timestamp: Optional[str] = None
