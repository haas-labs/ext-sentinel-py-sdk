# Detectors

Sentinel SDK includes several types of predefined detectors which can be used for building complex detectors

- Transaction Detector
- Block Detector

## Transaction Detector

The detector listens input transaction stream and invoke `on_transaction()` method for each transaction

```python
from sentinel.models.transaction import Transaction
from sentinel.processes.transaction import TransactionDetector

class TxDetector(TransactionDetector):
    async def on_transaction(self, transaction: Transaction) -> None:
        ...
```

## Block Detector

The detector listens input transaction stream, collects transactios per block, and when all transactions per block collected, invokes `on_block()` method. All transactions in a block ordered by transaction id

```python
from sentinel.processes.block import BlockDetector
from sentinel.models.transaction import Transaction

class BlockTxDetector(BlockDetector):
    async def on_block(self, transactions: List[Transaction]) -> None:
        ...
```

