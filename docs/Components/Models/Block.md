# Block Structure

| Field Name        | Field Type | Notes           |
| ----------------- | ---------- | --------------- |
| hash              | STRING     | Block Hash      |
| number            | INTEGER    | Block number    |
| timestamp         | INTEGER    | Block timestamp |
| parent_hash       | STRING     | Parent Hash     |
| nonce             | STRING     |                 |
| sha3_uncles       | STRING     |                 |
| logs_bloom        | STRING     |                 |
| transactions_root | STRING     |                 |
| state_root        | STRING     |                 |
| receipts_root     | STRING     |                 |
| miner             | STRING     |                 |
| difficulty        | INTEGER    |                 |
| total_difficulty  | INTEGER    |                 |
| size              | INTEGER    |                 |
| extra_data        | STRING     |                 |
| gas_limit         | INTEGER    |                 |
| gas_used          | INTEGER    |                 |
| base_fee_per_gas  | INTEGER    | Optional        |
| transaction_count | INTEGER    |                 |
