from sentinel.models.transaction import Transaction
from sentinel.sentry.transaction import TransactionDetector


class SimpleTxDetector(TransactionDetector):
    name = "SimpleTxDetector"

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        if transaction.value > 0:
            self.logger.info(transaction)
