import json
import pathlib
from typing import Dict

from sentinel.models.chains.vechain.transaction import VeChainLogEntry, VeChainTransaction


def test_vechain_transaction_load_sample_01():
    sample_01_path = pathlib.Path("tests/models/chains/vechain/resources/tx-01.json")
    json_tx = json.load(sample_01_path.open("r"))
    assert isinstance(json_tx, Dict), "Incorrect sample transaction type in raw JSON"

    tx = VeChainTransaction(**json_tx)
    assert isinstance(tx, VeChainTransaction), "Incorrect VeChain Transaction type"

    assert tx.transaction_index == 3, "Incorrect transaction index value"
    assert tx.timestamp == 1725115810000, "Incorrect timestamp value"
    assert tx.block_nbr == 19458766, "Incorrect block number value"
    assert tx.hash == "0xe80055beabefa8e72710b43aa817be36411549c32212dde34f3a4ee90d07a4a9", "Incorrect transaction hash"
    assert tx.size == 193, "Incorrect transaction size"
    assert tx.from_address == "0xe3d8f5d6c595cb7b0cf7daba7679670c95017275", "Incorrect transaction from address value"
    assert tx.to_address == "0x0000000000000000000000000000456e65726779", "Incorrect transaction to address value"
    assert tx.value == 0, "Incorrect value field"
    assert tx.nonce == "0x5c0027f39a0c8c12", "Incorrect nonce field value"
    assert tx.gas == 84000, "Incorrect gas field value"
    assert tx.gas_coefficient == 0, "Incorrect gas coefficient field value"
    assert tx.gas_used == 36518, "Incorrect gas used field value"
    assert tx.gas_payer == "0xe3d8f5d6c595cb7b0cf7daba7679670c95017275", "Incorrect gas payer field value"
    assert tx.gas_payed == 365180000000000000, "Incorrect gas payed field value"
    assert (
        tx.data
        == "0xa9059cbb000000000000000000000000600e221c9813a4ecdc4b57bf9e2b6ed6d14a3aa50000000000000000000000000000000000000000000000000ba8478cab540000"
    ), "Incorrect data field value"
    assert tx.expiration == 180, "Incorrect expiration field value"
    assert tx.delegator is None, "Incorrect delegator field value"
    assert tx.depends_on is None, "Incorrect depends_on field value"
    assert tx.reward == 109554000000000000, "Incorrect reward field value"
    assert tx.status is True, "Incorrect status field value"

    assert tx.logs == [
        VeChainLogEntry(
            address="0x0000000000000000000000000000456e65726779",
            data="0x0000000000000000000000000000000000000000000000000ba8478cab540000",
            topics=[
                "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
                "0x000000000000000000000000e3d8f5d6c595cb7b0cf7daba7679670c95017275",
                "0x000000000000000000000000600e221c9813a4ecdc4b57bf9e2b6ed6d14a3aa5",
            ],
        )
    ], "Incorrect transaction logs"
