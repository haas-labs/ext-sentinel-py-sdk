import pathlib
from typing import List

import pytest
from sentinel.channels.common import InboundChannel
from sentinel.core.v2.settings import Settings
from sentinel.models.transaction import Transaction
from sentinel.sentry.v2.block_tx import BlockTxDetector
from tx_generator import tx_generate


def test_block_tx_detector_init(tmpdir):
    local_tx_path = pathlib.Path(tmpdir / "transactions.jsonl")
    settings = Settings(
        inputs=[
            {
                "id": "local/fs/transactions",
                "type": "sentinel.channels.fs.transactions.InboundTransactionsChannel",
                "parameters": {"path": local_tx_path},
            },
        ]
    )

    detector = BlockTxDetector(
        settings=settings,
        parameters={
            "network": "ethereum",
        },
    )
    assert isinstance(detector, BlockTxDetector), "Incorrect Block Tx Detector type"
    assert detector.name == "BlockTxDetector", "Incorrect block tx detector name"
    assert detector.logger_name == "ethereum://BlockTxDetector", "Incorrect detector logger name"
    assert (
        detector.description
        == "The base block tx detector which can be used for mointoring activities in transactions stream when all transactions in a block are required during a one call and publishing results to events stream"
    )
    assert detector.databases is None, "Expect to have empty database list"

    detector.init()
    assert isinstance(detector.inputs.transactions, InboundChannel), "Incorrect inbound transactions channel"
    assert (
        detector.inputs.transactions.on_transaction == detector.on_transaction
    ), "Incorrect refs to on_transaction method"


@pytest.mark.asyncio
async def test_block_tx_detector_on_transaction():
    class Detector(BlockTxDetector):
        async def on_init(self) -> None:
            self.recevied_blocks = []

        async def on_block(self, transactions: List[Transaction]) -> None:
            block_id = transactions[0].block.number
            total_tx = len(transactions)
            self.recevied_blocks.append({"blk_num": block_id, "total_tx": total_tx})

    detector = Detector(
        parameters={
            "network": "ethereum",
        },
    )
    await detector.on_init()

    await detector.on_transaction(transaction=tx_generate(block_num=2, block_size=1, tx_index=0))
    assert detector.blocks_buffer == [], "Incorrect blocks buffer stats"
    assert detector.recevied_blocks == [{"blk_num": 2, "total_tx": 1}], "Incorrect received block stats"

    await detector.on_transaction(transaction=tx_generate(block_num=3, block_size=2, tx_index=0))
    assert detector.blocks_buffer == [
        {"blk_id": 3, "blk_size": 2, "txs": 1},
    ], "Incorrect blocks buffer stats"
    # Duplicated transaction
    await detector.on_transaction(transaction=tx_generate(block_num=3, block_size=2, tx_index=0))
    await detector.on_transaction(transaction=tx_generate(block_num=3, block_size=2, tx_index=1))
    assert detector.recevied_blocks == [
        {"blk_num": 2, "total_tx": 1},
        {"blk_num": 3, "total_tx": 2},
    ], "Incorrect received block stats"
    assert detector.blocks_buffer == [], "Incorrect blocks buffer stats"


@pytest.mark.asyncio
async def test_block_tx_detector_remove_outdated_blocks(tmpdir):
    class Detector(BlockTxDetector):
        async def on_init(self) -> None:
            self.recevied_blocks = []

        async def on_block(self, transactions: List[Transaction]) -> None:
            block_id = transactions[0].block.number
            total_tx = len(transactions)
            self.recevied_blocks.append({"blk_num": block_id, "total_tx": total_tx})

    local_tx_path = pathlib.Path(tmpdir / "transactions.jsonl")
    detector = Detector(
        parameters={
            "network": "ethereum",
        },
        settings=Settings(
            inputs=[
                {
                    "id": "local/fs/transactions",
                    "type": "sentinel.channels.fs.transactions.InboundTransactionsChannel",
                    "parameters": {"path": local_tx_path},
                },
            ]
        ),
    )
    detector.init()
    await detector.on_init()

    # Incomplete block
    await detector.on_transaction(transaction=tx_generate(block_num=1, block_size=2, tx_index=0))

    await detector.on_transaction(transaction=tx_generate(block_num=2, block_size=2, tx_index=0))
    await detector.on_transaction(transaction=tx_generate(block_num=2, block_size=2, tx_index=1))

    await detector.on_transaction(transaction=tx_generate(block_num=3, block_size=2, tx_index=0))
    await detector.on_transaction(transaction=tx_generate(block_num=3, block_size=2, tx_index=1))

    await detector.on_transaction(transaction=tx_generate(block_num=4, block_size=2, tx_index=0))
    await detector.on_transaction(transaction=tx_generate(block_num=4, block_size=2, tx_index=1))
    # Remove incompleted blocks with notification
    assert detector.blocks_buffer == [], "Incorrect blocks buffer stats"
