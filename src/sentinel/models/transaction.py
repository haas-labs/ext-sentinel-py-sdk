from typing import List, Optional
from pydantic import BaseModel, Field


class Block(BaseModel):
    """
    Transaction Block
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
    total_difficulty: int
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
    Transaction
    """

    type: Optional[str] = None
    hash: str
    nonce: int
    block: Block
    transaction_index: int
    from_address: Optional[str]
    to_address: Optional[str]
    value: int
    gas: int
    gas_price: int
    gas_used: int = Field(alias="receipt_gas_used")
    effective_gas_price: int = Field(alias="receipt_effective_gas_price")
    max_fee_per_gas: Optional[int] = None
    max_priority_fee_per_gas: Optional[int] = None
    cumulative_gas_used: int = Field(alias="receipt_cumulative_gas_used")
    input: str
    contract_address: Optional[str] = Field(alias="receipt_contract_address", default=None)
    root: Optional[str] = Field(alias="receipt_root")
    status: int = Field(alias="receipt_status")
    transaction_type: int
    logs: List[LogEntry]
    attack_probablity: float = 0.0
    item_id: Optional[str] = None
    item_timestamp: Optional[str] = None
