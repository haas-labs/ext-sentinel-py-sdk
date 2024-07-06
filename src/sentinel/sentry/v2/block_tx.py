from typing import Dict, List

from pydantic import BaseModel
from sentinel.core.v2.settings import Settings
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.transaction import TransactionDetector


class Block(BaseModel):
    """
    Block
    """

    size: int
    txs: Dict[int, Transaction]


class BlockTxDetector(TransactionDetector):
    name = "BlockTxDetector"
    description = """
        The base block tx detector which can be used for mointoring activities 
        in transactions stream when all transactions in a block are required 
        during a one call and publishing results to events stream
    """

    def __init__(
        self,
        name: str = None,
        description: str = None,
        restart: bool = True,
        schedule: str = None,
        parameters: Dict = dict(),
        monitoring_enabled: bool = False,
        monitoring_port: int = 9090,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            schedule=schedule,
            parameters=parameters,
            monitoring_enabled=monitoring_enabled,
            monitoring_port=monitoring_port,
            settings=settings,
            **kwargs,
        )

        # Blocks stack size
        self._blocks_stack_size = parameters.get("block_stack_size", 3)

        # Block storage
        self._blocks = dict()

    @property
    def blocks_buffer(self) -> List[Dict]:
        return [{"blk_id": _id, "blk_size": blk.size, "txs": len(blk.txs)} for _id, blk in self._blocks.items()]

    def _remove_outdated_blocks(self) -> None:
        """
        Remove outdated incomplete blocks
        """
        block_ids = list(self._blocks.keys())

        # if no blocks in a stack -> exit
        if len(block_ids) == 0:
            return

        last_block_id = max(block_ids)
        outdated_blocks = filter(lambda blk_id: last_block_id - blk_id >= self._blocks_stack_size, block_ids)
        for block_id in outdated_blocks:
            self._blocks.pop(block_id)

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

    # Handle Block Transactions
    async def on_block(self, transactions: List[Transaction]) -> None: ...
