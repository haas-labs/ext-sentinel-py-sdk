# Transaction Block Detector

`sentinel.sentry.v2.block_tx.BlockTxDetector`

The Transaction Block Detector is the way to build detectors/monitors when all transactions per block required for processing. This component leverages the `on_block()` method, which processes entire blocks of transactions instead of transactions, in comparison to [Transaction detector](TransactionDetector.md). 

It can handle operations like 
- block data summation
- analyzing transaction patterns within blocks
- processing where the sequence of transactions are important    
- or triggering batch processes based on block contents

## Event Handlers

- `on_block(self, transactions: List[Transaction])`: raised when all transactions per a block collected. 
  Transactions passed as argument

The detector listens input transaction stream, collects transactions per block, and when all transactions per block collected, invokes `on_block()` method. All transactions in a block ordered by transaction id

```python
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.block_tx import BlockTxDetector

class BlockTxDetector(BlockDetector):
    async def on_block(self, transactions: List[Transaction]) -> None:
        ...
```

## References

- [Transaction Block Detector Template](TransactionBlockDetectorTemplate.md)
