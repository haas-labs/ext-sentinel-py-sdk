from collections import Counter

from sentinel.models.transaction import Transaction
from sentinel.sentry.transaction import TransactionDetector


class SimpleTxMetricsDetector(TransactionDetector):
    name = "SimpleTxMetricsDetector"

    async def on_init(self):
        self.metrics = Counter()

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        if len(self.metrics) > 0 and self.metrics["total tx"] % 100 == 0:
            self.logger.info(self.metrics)

        match transaction.value:
            case 0:
                self.metrics["total tx with 0 value"] += 1
            case value if value > 0:
                self.metrics["total tx with value > 0"] += 1

        self.metrics["total tx"] += 1
