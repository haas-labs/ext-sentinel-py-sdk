import json

import pytest

from sentinel.models.transaction import Block, Transaction


@pytest.mark.parametrize(
    "file_path",
    [
        "tests/models/resources/tx-block-fail.json",
        "tests/models/resources/tx-block-success.json",
    ],
)
def test_block_message_parsing(file_path):
    block_data = json.load(open(file_path))
    print(block_data)
    block = Block(**block_data)
    assert block.total_difficulty == 58750003716598355984384


@pytest.mark.parametrize(
    "file_path",
    [
        "tests/models/resources/tx-fail.json",
        "tests/models/resources/tx-success.json",
    ],
)
def test_transaction_message_parsing(file_path):
    tx_data = json.load(open(file_path))
    transaction = Transaction(**tx_data)
    assert transaction.block.total_difficulty == 58750003716598355984384
