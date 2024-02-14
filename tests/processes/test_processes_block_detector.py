import json

import pytest
import pathlib

from typing import List


from sentinel.processes.block import BlockDetector
from sentinel.models.transaction import Transaction


def test_block_detector_init():
    """
    Test | Block Detector | Init
    """
    process = BlockDetector(
        name="TestBlockDetector",
        description="Test Block Detector",
    )

    assert isinstance(
        process, BlockDetector
    ), "Incorrect type for block detector instance"


@pytest.mark.asyncio
async def test_block_detector_collect_block_transactions():
    """
    Test | Block Detector | Collection block transactions

    sentinel fetch --rpc http://<json-rpc endpoint> \
                --dataset block \
                --from-file samples/block_transactions/data/blocks.list \
                --to-file samples/block_transactions/data/transactions.json
    
    blocks.list:
    - 0x1238cfe
    - 0x1238cff
    """

    async def on_block_hander(transactions: List[Transaction]) -> None:
        """
        Block handler
        """
        block_number = transactions[0].block.number
        match block_number:
            case 19107070:
                assert (
                    len(transactions) == 159
                ), f"Incorrect number of transactions for block: {block_number}"
            case 19107071:
                assert (
                    len(transactions) == 137
                ), f"Incorrect number of transactions for block: {block_number}"
            case _:
                assert False, f"Unknown block number: {block_number}"

    process = BlockDetector(
        name="TestBlockDetector",
        description="Test Block Detector",
    )
    process.on_block = on_block_hander

    for transaction in (
        pathlib.Path("tests/processes/resources/transactions.json")
        .open("r")
        .readlines()
    ):
        transaction = json.loads(transaction)
        await process.on_transaction(transaction=Transaction(**transaction))

@pytest.mark.asyncio
async def test_block_detector_incomplete_blocks_processing():
    """
    Test | Block Detector | Incomplete block processing
    """

    async def on_block_hander(transactions: List[Transaction]) -> None:
        """
        Block handler
        """
        block_number = transactions[0].block.number
        match block_number:
            case 5:
                assert (
                    len(transactions) == 2
                ), f"Incorrect number of transactions for block: {block_number}"
            case _:
                assert False, f"Unknown block number: {block_number}"

    process = BlockDetector(
        name="TestBlockDetector",
        description="Test Block Detector",
    )
    process.on_block = on_block_hander

    for transaction in (
        pathlib.Path("tests/processes/resources/incomplete-blocks.json")
        .open("r")
        .readlines()
    ):
        transaction = json.loads(transaction)
        await process.on_transaction(transaction=Transaction(**transaction))
