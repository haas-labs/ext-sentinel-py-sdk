# Transaction Detector

`sentinel.sentry.v2.transaction.TransactionDetector`

The Transaction Detector is most common way to build detectors/monitors around transactions. The component designed to process transactions in real-time. 

It operates by leveraging the `on_transaction()` method, which is triggered whenever a new transaction is detected on the Ethereum network. This method can be customized to perform a variety of operations, such as 
- logging transactions
- filtering based on specific criteria
- enrich transaction data by information from external resources
- store results of processing into local and external cache/databases
- or triggering further processing
    
## Event Handlers

- `on_transaction(self, transaction: Transaction)`: when new transaction received the method is called 
    and transaction passed as an argument

The detector listens input transaction stream and invoke `on_transaction()` method for each transaction

```python
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.transaction import TransactionDetector

class TxDetector(TransactionDetector):
    async def on_transaction(self, transaction: Transaction) -> None:
        ...
```

## Handling transaction logs

Transaction logs are a crucial part of Ethereum's event-driven architecture. They provide a detailed record of events that occurred during the execution of a transaction, especially when interacting with smart contracts. The Sentinel SDK natively supports ABI signatures for ERC20, ERC721, and ERC1155 standards, simplifying operations with events.

```python
# For each transaction, we are checking if there is ERC20 TRANSFER event in logs
for event in filter_events(transaction.logs, [ABI_EVENT_TRANSFER]):
   from_address = event.fields.get("from")
   to_address = event.fields.get("to")
   value = event.fields.get("value")
```
## References

- [Transaction Detector Template](TransactionDetectorTemplate.md)
