# Transaction Detector

`sentinel.sentry.v2.transaction.TransactionDetector`

The Transaction Detector is most common way to build detectors/monitors around transactions.

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

## References

- [Transaction Model](/src/sentinel/models/transaction.py)
