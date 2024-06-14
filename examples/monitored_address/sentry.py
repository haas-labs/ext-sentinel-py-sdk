from sentinel.metrics.counter import Counter
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.transaction import TransactionDetector


class MonitoredAddressTxDetector(TransactionDetector):
    name = "TxMetricsDetector"

    async def on_init(self):
        self.metrics.register(
            Counter(
                name="transactions_total",
                doc="Total number of incoming transactions",
                labels={"detector": self.name, "network": self.network},
            )
        )
        self.metrics.register(
            Counter(
                name="transactions_zero_value_total",
                doc="Total number of transactions with 0 value",
                labels={"detector": self.name, "network": self.network},
            )
        )
        self.metrics.register(
            Counter(
                name="transactions_value_gt_zero_total",
                doc="Total number of transactions with value greater than 0",
                labels={"detector": self.name, "network": self.network},
            )
        )

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        self.metrics.transactions_total.inc()

        match transaction.value:
            case 0:
                self.metrics.transactions_zero_value_total.inc()
            case value if value > 0:
                self.metrics.transactions_value_gt_zero_total.inc()
