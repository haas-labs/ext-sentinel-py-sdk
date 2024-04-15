import time

from sentinel.metrics.counter import Counter
from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction
from sentinel.sentry.transaction import TransactionDetector


class SimpleTxMetricsDetector(TransactionDetector):
    name = "SimpleTxMetricsDetector"

    async def on_init(self):
        self.metrics.register(
            Counter(name="transactions_total", doc="Total number of transactions", labels={"detector": self.name})
        )
        self.metrics.register(
            Counter(
                name="transactions_with_zero_value_total",
                doc="Total number of transactions with zero value",
                labels={"detector": self.name},
            )
        )
        self.metrics.register(
            Counter(
                name="transactions_with_value_gt_zero_total",
                doc="Total number of transactions with zero value",
                labels={"detector": self.name},
            )
        )

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        self.metrics.get("transactions_total").inc()

        match transaction.value:
            case 0:
                self.metrics.get("transactions_with_zero_value_total").inc()
            case value if value > 0:
                self.metrics.get("transactions_with_value_gt_zero_total").inc()

        if transaction.value == 0:
            return

        await self.outputs.events.send(
            Event(
                did="transactions",
                type="test_event",
                severity=0.01,
                ts=int(time.time() * 1000),
                blockchain=Blockchain(network="ethereum", chain_id="1"),
                metadata={
                    "tx_hash": transaction.hash,
                    "value": transaction.value,
                },
            )
        )
