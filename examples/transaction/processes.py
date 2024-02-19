import logging

from sentinel.models.transaction import Transaction
from sentinel.processes.transaction import TransactionDetector

logger = logging.getLogger(__name__)

class SimpleTxDetector(TransactionDetector):
    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions with value > 0
        """
        if transaction.value > 0:
            logger.info(transaction)
