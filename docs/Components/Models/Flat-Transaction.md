# Flat Transactions

To store an Ethereum transaction model in a Relational Database Management System (RDBMS) more effectively, the model should be flattened, and relationships between different entities (e.g., transactions, logs, blocks) should be clearly defined. This involves converting nested structures into separate tables with foreign keys to maintain relationships.

## Flattening Considerations

- **Block information**: Instead of embedding the block within the transaction, we reference it using `block_hash`. The `blocks` table stores all block details.
- **Logs**: The `log_entries` table references the transaction (`transaction_hash`) and stores individual logs. Each log can have multiple topics, stored in the `log_topics` table.
- **Gas-related fields**: All gas-related fields are kept in the `transactions` table, as they are directly related to each transaction.
- **Optional fields**: Fields like `max_fee_per_gas`, `max_priority_fee_per_gas`, `contract_address`, and `root` are optional, so they can be `NULL` in the database.
- **Attack probability**: This is a custom field, and it's included directly in the `transactions` table with a default value of `0.0`.

## Blocks Table

| Field Name        | Field Type    | Description                                             |
|-------------------|---------------|---------------------------------------------------------|
| hash              | VARCHAR       | Unique identifier for the block.                        |
| number            | INTEGER       | Block number in the blockchain.                         |
| timestamp         | TIMESTAMP     | Time when the block was mined.                          |
| parent_hash       | VARCHAR       | Hash of the previous block.                             |
| nonce             | VARCHAR       | Value used for mining the block (proof of work).       |
| sha3_uncles       | VARCHAR       | SHA3 hash of the uncles (omitted blocks) in the block.|
| logs_bloom        | VARCHAR       | Bloom filter for logs in the block.                     |
| transactions_root | VARCHAR       | Root hash of the transactions in the block.            |
| state_root        | VARCHAR       | Root hash of the state after the block is processed.   |
| receipts_root     | VARCHAR       | Root hash of the receipts in the block.                |
| miner             | VARCHAR       | Address of the miner who mined the block.              |
| difficulty        | INTEGER       | Difficulty of the block.                                |
| total_difficulty   | INTEGER      | Total difficulty of the blockchain up to this block.   |
| size              | INTEGER       | Size of the block in bytes.                             |
| extra_data        | VARCHAR       | Extra data included in the block.                       |
| gas_limit         | INTEGER       | Maximum gas limit for transactions in the block.       |
| gas_used          | INTEGER       | Total gas used by all transactions in the block.       |
| base_fee_per_gas  | INTEGER       | Base fee per gas for transactions (if applicable).     |
| transaction_count  | INTEGER      | Number of transactions included in the block.          |

## Transactions Table

| Field Name               | Field Type    | Description                                                   |
|--------------------------|---------------|---------------------------------------------------------------|
| hash                     | VARCHAR       | Unique identifier for the transaction.                        |
| has_input                | BOOLEAN       | Indicates whether the transaction has an input.               |
| nonce                    | INTEGER       | Nonce of the transaction.                                    |
| block_hash               | VARCHAR       | Hash of the block that includes the transaction.              |
| transaction_index        | INTEGER       | Index of the transaction within the block.                   |
| from_address             | VARCHAR       | Sender's Ethereum address.                                   |
| to_address               | VARCHAR       | Receiver's Ethereum address (optional for contract creation). |
| value                    | BIGINT        | Amount of Ether transferred.                                  |
| gas                      | INTEGER       | Gas limit for the transaction.                                |
| gas_price                | INTEGER       | Gas price for the transaction.                                |
| gas_used                 | INTEGER       | Gas used by the transaction.                                  |
| effective_gas_price      | INTEGER       | Effective gas price used for the transaction.                |
| max_fee_per_gas         | INTEGER       | Maximum fee per gas the sender is willing to pay.            |
| max_priority_fee_per_gas | INTEGER       | Maximum priority fee per gas.                                 |
| cumulative_gas_used      | INTEGER       | Cumulative gas used by all transactions in the block.        |
| contract_address         | VARCHAR       | Address of the contract created by the transaction (if any). |
| root                     | VARCHAR       | Merkle root of the transaction data (if applicable).        |
| status                   | INTEGER       | Status of the transaction (0 for failure, 1 for success).    |
| transaction_type         | INTEGER       | Type of transaction (e.g., standard, contract creation).     |
| log_entries              | INTEGER       | Number of log entries generated by the transaction.           |
| timestamp                | TIMESTAMP     | Time when the transaction was mined.                          |

## Transaction Inputs Table

| Field Name       | Field Type | Description                                   |
| ---------------- | ---------- | --------------------------------------------- |
| transaction_hash | VARCHAR    | Unique identifier for the transaction.        |
| input_data       | TEXT       | Input data for the transaction, can be large. |
| has_data         | BOOLEAN    | Indicates whether the input data exists.      |

## Log Entries Table

| Field Name | Field Type | Description                                     |
| ---------- | ---------- | ----------------------------------------------- |
| index      | INTEGER    | Index of the log entry in the transaction.      |
| address    | VARCHAR    | Address of the contract that generated the log. |
| data       | TEXT       | Log data associated with the transaction.       |
| topics     | TEXT[]     | Array of topics associated with the log entry.  |
