import pytest

from sentinel.utils.bytecode import Bytecode


def test_bytecode_init():
    bytecode = Bytecode(bytecode="0x123456")
    assert isinstance(bytecode, Bytecode), "Incorrect bytecode type"


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
    bytecode = Bytecode(
        bytecode="0x60806040...00080fd5b5035919050565b600060208284031215610ad357600080fd5b610adc82610a26565b9392505050565b60008060408385031215610af657600080fd5b610aff83610a26565b9150610b0d60208401610a26565b90509250929050565b600181811c90821680610b2a57607f821691505b602082108103610b4a57634e487b7160e01b600052602260045260246000fd5b50919050565b808201808211156102fb57634e487b7160e01b600052601160045260246000fdfea2646970667358221220752c1a7264033a67519f23022e2c375079c74dab80b9c0492dc8a9a57c332c6364736f6c63430008120033"
    )
    metadata = bytecode.metadata
    # re-use early calculated metadata
    metadata = bytecode.metadata
    assert (
        metadata.data
        == "a2646970667358221220752c1a7264033a67519f23022e2c375079c74dab80b9c0492dc8a9a57c332c6364736f6c6343000812"
    ), "Incorrect metadata raw data"
    assert metadata.length == 51, "Incorrect metadata length"
    assert (
        metadata.ipfs == "1220752c1a7264033a67519f23022e2c375079c74dab80b9c0492dc8a9a57c332c63"
    ), "Incorrect IPFS value"
    assert metadata.solc == [0, 8, 18], "Incorrect SOLC value"
