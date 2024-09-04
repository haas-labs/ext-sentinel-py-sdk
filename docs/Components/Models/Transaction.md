# Transaction Structure

This data model captures the essential details of an Ethereum transaction by consolidating information from the transaction, block, and receipt RPC messages. The model is designed to be comprehensive yet flexible, allowing for efficient validation and interpretation of transaction data

| Field Name               | Field Type                      | Notes                                  |
| ------------------------ | ------------------------------- | -------------------------------------- |
| hash                     | STRING                          | Transaction Hash                       |
| nonce                    | INTEGER                         |                                        |
| block                    | [Block](Block.md)               |                                        |
| transaction_index        | INTEGER                         |                                        |
| from_address             | STRING                          |                                        |
| to_address               | STRING                          |                                        |
| value                    | INTEGER                         |                                        |
| gas                      | INTEGER                         |                                        |
| gas_price                | INTEGER                         |                                        |
| gas_used                 | INTEGER                         | Alias to `receipt_gas_used`            |
| effective_gas_price      | INTEGER                         | Alias to `receipt_effective_gas_price` |
| max_fee_per_gas          | INTEGER                         |                                        |
| max_priority_fee_per_gas | INTEGER                         |                                        |
| cumulative_gas_used      | INTEGER                         | Alias to `receipt_cumulative_gas_used` |
| input                    | STRING                          |                                        |
| contract_address         | STRING                          | Alias to `receipt_contract_address`    |
| root                     | STRING                          | Alias to `receipt_root`                |
| status                   | INTEGER                         | Alias to `receipt_status`              |
| transaction_type         | INTEGER                         |                                        |
| logs                     | List <[Log Entry](LogEntry.md)> |                                        |
| attack_probablity        | FLOAT                           | Default: 0.0                           |
