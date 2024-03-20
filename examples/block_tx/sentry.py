import logging

from typing import List

from collections import defaultdict

from sentinel.sentry.block import BlockDetector

from sentinel.models.event import Event, Blockchain
from sentinel.models.transaction import Transaction


logger = logging.getLogger(__name__)


class BlockTxDetector(BlockDetector):
    async def on_block(self, transactions: List[Transaction]) -> None:
        """
        Handle block transactions
        """
        selected_transactions = dict()
        to_from_pairs = defaultdict(list)

        for tx in transactions:
            if not self.databases["dex_addresses"].exists(tx.to_address):
                continue
            selected_transactions[tx.hash] = tx
            to_from_pairs[tx.to_address, tx.from_address].append({"hash": tx.hash, "gas_price": tx.gas_price})
            if len(to_from_pairs[tx.to_address, tx.from_address]) == 2:
                tx1, tx2 = to_from_pairs[tx.to_address, tx.from_address]
                if tx1["gas_price"] != tx2["gas_price"]:
                    await self.send_notification(selected_transactions[tx1["hash"]])
                    await self.send_notification(selected_transactions[tx2["hash"]])

    async def send_notification(self, transaction: Transaction) -> None:
        """
        Send notification about potential block_tx transaction
        """
        logger.warning(f"Detected block_tx transaction: {transaction.hash}")
        await self.channels["events"].send(
            Event(
                did=self.detector_name,
                type="potential_block_tx_tx_detected",
                severity=0.3,
                ts=transaction.block.timestamp * 1000,
                blockchain=Blockchain(
                    network=self.parameters["network"],
                    chain_id=str(self.parameters["chain_id"]),
                ),
                metadata={
                    "tx_hash": transaction.hash,
                    "tx_from": transaction.from_address,
                    "tx_to": transaction.to_address,
                    "desc": "Potential block_tx transaction detected",
                },
            )
        )
