# Transaction Block Detector Template

The example of simple detector based on `TransactionDetector` class

```python
from collections import Counter
from typing import List

from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.block_tx import BlockTxDetector


class TransactionBlockDetectorTemplate(BlockTxDetector):
    name = "TransactionBlockDetectorTemplate"
    description = "The template for building detectors based on TransactionBlockDetector class"
    
	async def on_init(self) -> None:
        self.log_metrics = Counter()
        
    async def on_block(self, transactions: List[Transaction]) -> None:
        """
        Handle block transactions
        """
        self.log_metrics["total_blocks"] += 1
        if self.log_metrics["total_blocks"] % 100 == 0:
            self.logger.info(self.log_metrics)

        for tx in transactions:
            self.log_metrics["total_transactions"] += 1

```
