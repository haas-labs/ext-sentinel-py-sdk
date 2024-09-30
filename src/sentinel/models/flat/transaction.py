from typing import List, Optional

from pydantic import BaseModel, Field


class Block(BaseModel):
    """
    EVM Based Transaction Block
    """

    hash: str = Field(..., description="Unique identifier for the block (block hash)")
    number: int = Field(..., description="Block number in the blockchain")
    timestamp: int = Field(..., description="Unix timestamp indicating when the block was mined")
    parent_hash: str = Field(..., description="Hash of the parent block")
    nonce: str = Field(..., description="Proof of work nonce for the block")
    sha3_uncles: str = Field(..., description="Hash of the uncles (or ommers) included in the block")
    logs_bloom: str = Field(..., description="Bloom filter for quick searching of logs included in the block")
    transactions_root: str = Field(..., description="Hash of the root node of the transactions trie")
    state_root: str = Field(..., description="Hash of the root node of the state trie")
    receipts_root: str = Field(..., description="Hash of the root node of the receipts trie")
    miner: str = Field(..., description="Address of the miner who mined the block")
    difficulty: int = Field(..., description="Difficulty level of mining the block")
    total_difficulty: int = Field(..., description="Cumulative difficulty of the chain until this block")
    size: int = Field(..., description="Size of the block in bytes")
    extra_data: str = Field(..., description="Extra data included by the miner")
    gas_limit: int = Field(..., description="Maximum amount of gas allowed in the block")
    gas_used: int = Field(..., description="Total gas used by all transactions in the block")
    base_fee_per_gas: Optional[int] = Field(None, description="Base fee per gas for EIP-1559 transactions (optional)")
    transaction_count: int = Field(..., description="Number of transactions in the block")


class LogEntry(BaseModel):
    """
    Merged Log Entry and Topics
    """

    id: Optional[int] = Field(None, description="Unique identifier for the log entry")
    transaction_hash: str = Field(..., description="Hash of the transaction this log entry belongs to")
    log_index: int = Field(..., description="Position of the log entry in the transaction")
    address: str = Field(..., description="Address of the contract that emitted the log")
    data: str = Field(..., description="Data contained in the log entry")
    topics: List[str] = Field(default_factory=list, description="Array of topics associated with the log entry")


class TransactionInput(BaseModel):
    """
    Transaction Input Data
    """

    transaction_hash: str = Field(..., description="Hash of the transaction this input belongs to")
    input_data: str = Field(..., description="Input data for contract calls or contract creation")


class Transaction(BaseModel):
    """
    EVM based Transaction
    """

    hash: str = Field(..., description="Unique identifier for the transaction (transaction hash)")
    nonce: int = Field(..., description="Number of transactions sent from the sender's address")
    block: Block = Field(..., description="The block containing this transaction")
    transaction_index: int = Field(..., description="Position of the transaction within the block")
    from_address: Optional[str] = Field(None, description="Address of the sender")
    to_address: Optional[str] = Field(
        None, description="Address of the recipient (could be null for contract creation)"
    )
    value: int = Field(..., description="Amount of Ether transferred in the transaction (in Wei)")
    gas: int = Field(..., description="Gas limit for the transaction")
    gas_price: int = Field(..., description="Price per unit of gas (in Wei)")
    gas_used: int = Field(..., description="Amount of gas used by the transaction")
    effective_gas_price: Optional[int] = Field(
        None, description="Actual price per unit of gas paid after execution (for EIP-1559 transactions)"
    )
    max_fee_per_gas: Optional[int] = Field(None, description="Maximum fee per gas specified for EIP-1559 transactions")
    max_priority_fee_per_gas: Optional[int] = Field(
        None, description="Max priority fee per gas for the miner (optional)"
    )
    cumulative_gas_used: int = Field(..., description="Total gas used in the block up to this transaction")
    has_input: bool = Field(..., description="Indicates whether the transaction has associated input data")
    contract_address: Optional[str] = Field(
        None, description="Address of the contract created by the transaction (optional)"
    )
    root: Optional[str] = Field(
        None, description="State root after transaction execution (optional, included in older receipts)"
    )
    status: int = Field(..., description="Status of the transaction (1 for success, 0 for failure)")
    transaction_type: Optional[int] = Field(
        None, description="Type of transaction (0 for legacy, 1 for EIP-1559, etc.)"
    )
    log_entries: int = Field(..., description="Number of log entries associated with the transaction")
    attack_probability: float = Field(0.0, description="Probability of the transaction being an attack (custom field)")


# SQL

SQL_CREATE_BLOCKS_TABLE = """
CREATE TABLE IF NOT EXISTS blocks (
    hash VARCHAR PRIMARY KEY, -- Unique identifier for the block (block hash)
    number INTEGER, -- Block number in the blockchain
    timestamp BIGINT, -- Unix timestamp indicating when the block was mined
    parent_hash VARCHAR, -- Hash of the parent block
    nonce VARCHAR, -- Proof of work nonce for the block
    sha3_uncles VARCHAR, -- Hash of the uncles (or ommers) included in the block
    logs_bloom VARCHAR, -- Bloom filter for quick searching of logs included in the block
    transactions_root VARCHAR, -- Hash of the root node of the transactions trie
    state_root VARCHAR, -- Hash of the root node of the state trie
    receipts_root VARCHAR, -- Hash of the root node of the receipts trie
    miner VARCHAR, -- Address of the miner who mined the block
    difficulty BIGINT, -- Difficulty level of mining the block
    total_difficulty BIGINT, -- Cumulative difficulty of the chain until this block
    size INTEGER, -- Size of the block in bytes
    extra_data VARCHAR, -- Extra data included by the miner
    gas_limit BIGINT, -- Maximum amount of gas allowed in the block
    gas_used BIGINT, -- Total gas used by all transactions in the block
    base_fee_per_gas BIGINT, -- Base fee per gas for EIP-1559 transactions (optional)
    transaction_count INTEGER -- Number of transactions in the block
);
"""

SQL_CREATE_LOG_ENTRIES_TABLE = """
CREATE TABLE IF NOT EXISTS log_entries (
    id SERIAL PRIMARY KEY, -- Unique identifier for the log entry
    transaction_hash VARCHAR REFERENCES transactions(hash), -- Hash of the transaction this log entry belongs to
    log_index INTEGER, -- Position of the log entry in the transaction
    address VARCHAR, -- Address of the contract that emitted the log
    data TEXT, -- Data contained in the log entry
    topics TEXT[] -- Array of topics associated with the log entry
);
"""

SQL_CREATE_TRANSACTIONS_TABLE = """"
CREATE TABLE IF NOT EXISTS transactions (
    hash VARCHAR PRIMARY KEY, -- Unique identifier for the transaction (transaction hash)
    nonce INTEGER, -- Number of transactions sent from the sender's address
    block_hash VARCHAR REFERENCES blocks(hash), -- Hash of the block that contains this transaction
    transaction_index INTEGER, -- Position of the transaction within the block
    from_address VARCHAR, -- Address of the sender
    to_address VARCHAR, -- Address of the recipient (could be null for contract creation)
    value BIGINT, -- Amount of Ether transferred in the transaction (in Wei)
    gas BIGINT, -- Gas limit for the transaction
    gas_price BIGINT, -- Price per unit of gas (in Wei)
    gas_used BIGINT, -- Amount of gas used by the transaction
    effective_gas_price BIGINT, -- Actual price per unit of gas paid after execution (for EIP-1559 transactions)
    max_fee_per_gas BIGINT, -- Maximum fee per gas specified for EIP-1559 transactions (optional)
    max_priority_fee_per_gas BIGINT, -- Max priority fee per gas for the miner (optional)
    cumulative_gas_used BIGINT, -- Total gas used in the block up to this transaction
    contract_address VARCHAR, -- Address of the contract created by the transaction (optional)
    root VARCHAR, -- State root after transaction execution (optional, included in older receipts)
    status INTEGER, -- Status of the transaction (1 for success, 0 for failure)
    transaction_type INTEGER, -- Type of transaction (0 for legacy, 1 for EIP-1559, etc.)
    has_input BOOLEAN NOT NULL DEFAULT FALSE, -- Indicates whether the transaction has associated input data
    log_entries INTEGER, -- Number of log entries associated with the transaction
    attack_probability FLOAT DEFAULT 0.0 -- Probability of the transaction being an attack (custom field)
    timestamp TIMESTAMP NOT NULL,  -- Ensure you have a timestamp for partitioning
) PARTITION BY RANGE (timestamp);
CREATE INDEX idx_has_input ON transactions(has_input);
"""

SQL_CREATE_TRANSACTION_INPUTS_TABLE = """
CREATE TABLE transaction_inputs (
    transaction_hash VARCHAR PRIMARY KEY REFERENCES transactions(hash), -- Foreign key to transactions
    input_data TEXT -- Input data for contract calls or contract creation (potentially large)
);
CREATE INDEX idx_transaction_hash ON transaction_inputs(transaction_hash);
ALTER TABLE transaction_inputs ADD CONSTRAINT fk_transaction FOREIGN KEY (transaction_hash) REFERENCES transactions(hash);
"""
