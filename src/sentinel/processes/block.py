from typing import Dict, List

from pydantic import BaseModel

from sentinel.models.transaction import Transaction
from sentinel.processes.transaction import TransactionDetector


class Block(BaseModel):
    """
    Block
    """

    size: int
    txs: Dict[int, Transaction]


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
        self._blocks_stack_size = parameters.get("block_stack_size", 3)

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

        queued_blocks = {}
        for blk_id, blk_meta in self._blocks.items():
            if last_blk_num - blk_id < self._blocks_stack_size:
                queued_blocks[blk_id] = blk_meta
            else:
                logger.warning(
                    f"Incomplete block detected, block id: {blk_id}, "
                    + f"expected tx: {blk_meta.size}, "
                    + f"detected tx: {len(blk_meta.txs)}"
                )
        self._blocks = queued_blocks

    async def on_transaction(self, transaction: Transaction) -> None:
        """
        Handle Transaction
        """
        # Cleanup outdated incomplete blocks
        self._remove_outdated_blocks()

        # block and transaction parameters
        block_number = transaction.block.number
        block_size = transaction.block.transaction_count
        tx_index = transaction.transaction_index

        if block_number not in self._blocks:
            # if block is new
            self._blocks[block_number] = Block(
                size=block_size,
                txs={tx_index: transaction},
            )
        else:
            # duplicated transaction detected
            if tx_index in self._blocks[block_number].txs:
                return
            # Add transactions to a block storage
            self._blocks[block_number].txs[tx_index] = transaction

        # Check if the block is full
        if len(self._blocks[block_number].txs) != block_size:
            return

        # The block is full, sort transactions and call on_block() handler
        block = self._blocks.pop(block_number)
        txs = list()
        for _tx_index in range(block_size):
            txs.append(block.txs[_tx_index])
        await self.on_block(txs)

    async def on_block(self, transactions: List[Transaction]) -> None:
        """
        Handle Block Transactions
        """
        pass
