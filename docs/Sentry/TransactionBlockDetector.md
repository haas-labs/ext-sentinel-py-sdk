# Transaction Block Detector

`sentinel.sentry.v2.block_tx.BlockTxDetector`

The Transaction Block Detector is the way to build detectors/monitors when all transactions per block 
required for processing.

## Event Handlers

- `on_block(self, transactions: List[Transaction])`: raised when all transactions per a block collected. 
  Transactions passed as argument

## References

- [Transaction Model](/src/sentinel/models/transaction.py)
