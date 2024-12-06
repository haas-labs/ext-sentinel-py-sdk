import pytest

from sentinel.utils.bytecode import Bytecode, HashType

BYTECODE_SAMPLE = "0x6080604000080fd5b5035919050565b600060208284031215610ad357600080fd5b610adc82610a26565b9392505050565b60008060408385031215610af657600080fd5b610aff83610a26565b9150610b0d60208401610a26565b90509250929050565b600181811c90821680610b2a57607f821691505b602082108103610b4a57634e487b7160e01b600052602260045260246000fd5b50919050565b808201808211156102fb57634e487b7160e01b600052601160045260246000fdfea2646970667358221220752c1a7264033a67519f23022e2c375079c74dab80b9c0492dc8a9a57c332c6364736f6c63430008120033"


def test_bytecode_init():
    bytecode = Bytecode(bytecode="0x123456")
    assert isinstance(bytecode, Bytecode), "Incorrect bytecode type"


def test_bytecode_init_without_0x():
    with pytest.raises(ValueError):
        Bytecode(bytecode="123456")


def test_bytecode_init_error_handling():
    with pytest.raises(ValueError) as err:
        Bytecode(bytecode=None)
    assert str(err.value) == "Empty bytecode", "Incorrect error message"

    with pytest.raises(ValueError) as err:
        Bytecode(bytecode="0x")
    assert str(err.value) == "Empty bytecode", "Incorrect error message"


# def test_bytecode_get_ipfs_hash():
#     ipfs_bytes = "1220c019e4614043d8adc295c3046ba5142c603ab309adeef171f330c51c38f14989"
#     assert (
#         Bytecode.get_ipfs_hash(bytes.fromhex(ipfs_bytes)) == "QmbGXtNqvZYEcbjK6xELyBQGEmzqXPDqyJNoQYjJPrST9S"
#     ), "Incorrect IPFS hash"


def test_bytecode_extract_metadata():
    bytecode = Bytecode(bytecode=BYTECODE_SAMPLE)
    metadata = bytecode.metadata
    # re-use early calculated metadata
    metadata = bytecode.metadata
    assert (
        metadata.data
        == "a2646970667358221220752c1a7264033a67519f23022e2c375079c74dab80b9c0492dc8a9a57c332c6364736f6c6343000812"
    ), "Incorrect metadata raw data"
    assert metadata.length == 51, "Incorrect metadata length"
    assert metadata.ipfs == "QmWE3R3YMFsqA6mZTtAY8xgPeqh2xnQMuMR7cRk95atati", "Incorrect IPFS value"
    assert metadata.solc == [0, 8, 18], "Incorrect SOLC value"


def test_bytecode_calculate_hash():
    bytecode = Bytecode(bytecode=BYTECODE_SAMPLE)
    assert (
        bytecode.contract_hash(hash_type=HashType["KECCAK"]).hex()
        == "d1e264d0fda3e9267ad33a9bdae70258117c03e94537e44692f321a1022f490f"
    ), "Incorrect contract KECCAK hash"
    assert (
        bytecode.contract_hash(hash_type=HashType["SHA256"]).hex()
        == "d5e92aa61e7b8753adfc2fe46ff542337025d99378197c885d2b74543e4a6cab"
    ), "Incorrect contract SHA256 hash"


def test_bytecode_unsupported_hash_type():
    bytecode = Bytecode(bytecode=BYTECODE_SAMPLE)
    with pytest.raises(ValueError) as err:
        bytecode.contract_hash(hash_type="UNSUPPORTED_HASH")
    assert (
        str(err.value) == "Unsupported hash type: UNSUPPORTED_HASH"
    ), "Incorrect error message for unsupported hash type"
