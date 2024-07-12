# Transaction Detector Template

The example of simple detector based on `TransactionDetector` class

```python
from collections import Counter
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.transaction import TransactionDetector


class TransactionDetectorTemplate(TransactionDetector):
    name = "TransactionDetectorTemplate"
    description = "The template for building detectors based on TransactionDetector class"
    
	async def on_init(self) -> None:
        self.log_metrics = Counter()
        
    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        self.log_metrics["total_transactions"] += 1
        if self.log_metrics["total_transactions"] % 1000 == 0:
            self.logger.info(self.log_metrics)

        match transaction.value:
            case 0:
                self.log_metrics["total_transactions_zero_value"] += 1
            case value if value > 0:
                self.log_metrics["total_transactions_value_gt_zero"] += 1
```