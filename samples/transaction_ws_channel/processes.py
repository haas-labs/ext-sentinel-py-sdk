import logging


from sentinel.models.transaction import Transaction
from sentinel.processes.transaction import TransactionDetector


logger = logging.getLogger(__name__)


class SimpleTxDetector(TransactionDetector):
    """
    Simple Transaction Detector
    """
    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle transactions
        """
        logger.info(transaction)
