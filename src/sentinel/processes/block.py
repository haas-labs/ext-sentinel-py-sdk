import logging


from typing import Dict, List

from pydantic import BaseModel

from sentinel.models.transaction import Transaction
from sentinel.processes.transaction import TransactionDetector


logger = logging.getLogger(__name__)


class BlockTransactions(BaseModel):
    """
    BlockTransactions
    """

    transaction_count: int
    transactions: Dict[int, Transaction]


class BlockDetector(TransactionDetector):
    """
    Block Detector
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        inputs: Dict = dict(),
        outputs: Dict = dict(),
        databases: Dict = dict(),
        parameters: Dict = dict(),
    ) -> None:
        """
        Block Detector Init
        """
        super().__init__(name, description, inputs, outputs, databases, parameters)

        # Blocks stack size
        self._blocks_stack_size = parameters.get("block_stack_size", 10)

        # Block storage
        self._blocks = dict()

    def _remove_outdated_blocks(self) -> None:
        """
        Remove outdated incomplete blocks
        """
        blk_numbers = self._blocks.keys()

        # if no blocks in a stack -> exit
        if len(blk_numbers) == 0:
            return

        last_blk_num = max(blk_numbers)

        self._blocks = {k: v for k, v in self._blocks.items() if last_blk_num - k < self._blocks_stack_size}

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        # Cleanup outdated incomplete blocks
        self._remove_outdated_blocks()

        # block and transaction parameters
        block_number = transaction.block.number
        transaction_count = transaction.block.transaction_count
        tx_index = transaction.transaction_index

        block_stats = {blk_id: len(self._blocks[blk_id].transactions) for blk_id in self._blocks}
        logger.info(f"Blocks: {block_stats}")

        # new block detected
        if block_number not in self._blocks:
            self._blocks[block_number] = BlockTransactions(
                transaction_count=transaction_count,
                transactions={tx_index: transaction},
            )
        else:
            # duplicated transaction detected
            if tx_index in self._blocks[block_number].transactions:
                return
            # Add transactions to a block storage
            self._blocks[block_number].transactions[tx_index] = transaction

        # Check if the block is full
        if len(self._blocks[block_number].transactions) != transaction_count:
            return

        # The block is full, sort transactions and call on_block() handler
        block = self._blocks.pop(block_number)
        transactions = list()
        for _tx_index in range(transaction_count):
            transactions.append(block.transactions[_tx_index])
        await self.on_block(transactions)

    async def on_block(self, transactions: List[Transaction]) -> None:
        """
        Handle Block Transactions
        """
        pass
