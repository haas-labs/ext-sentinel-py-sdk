import pathlib
from sentinel.utils.bytecode import Bytecode


def test_bytecode_cgrt_token_compare_chain_and_get_code():
    chain_bytecode = Bytecode(pathlib.Path("tests/utils/resources/bytecode/cgpt_token/chain.bytecode").open().read())
    chain_metadata = chain_bytecode.metadata

    get_code_bytecode = Bytecode(
        pathlib.Path("tests/utils/resources/bytecode/cgpt_token/get_code.bytecode").open().read()
    )
    get_code_metadata = get_code_bytecode.metadata

    assert chain_bytecode.contract_hash == get_code_bytecode.contract_hash, "Contract hash mismatch"
    assert chain_metadata.ipfs == get_code_metadata.ipfs, "IPFS hash mismatch"
    assert chain_metadata.solc == get_code_metadata.solc, "SOLC version mismatch"


def test_bytecode_cgrt_token_compare_chain_and_compiled_paris_0_8_18():
    chain_bytecode = Bytecode(pathlib.Path("tests/utils/resources/bytecode/cgpt_token/chain.bytecode").open().read())
    chain_metadata = chain_bytecode.metadata

    compiled_bytecode = Bytecode(
        pathlib.Path("tests/utils/resources/bytecode/cgpt_token/compiled-paris-0.8.18.bytecode").open().read()
    )
    compiled_metadata = compiled_bytecode.metadata

    assert chain_bytecode.contract_hash == compiled_bytecode.contract_hash, "Contract hash mismatch"
    # assert chain_metadata.ipfs == compiled_metadata.ipfs, "IPFS hash mismatch"
    assert chain_metadata.solc == compiled_metadata.solc, "SOLC version mismatch"


def test_bytecode_cgrt_token_compare_chain_and_compiled_paris_0_8_24():
    chain_bytecode = Bytecode(pathlib.Path("tests/utils/resources/bytecode/cgpt_token/chain.bytecode").open().read())
    # chain_metadata = chain_bytecode.metadata

    compiled_bytecode = Bytecode(
        pathlib.Path("tests/utils/resources/bytecode/cgpt_token/compiled-paris-0.8.24.bytecode").open().read()
    )
    # compiled_metadata = compiled_bytecode.metadata

    assert chain_bytecode.contract_hash != compiled_bytecode.contract_hash, "Contract hash mismatch"
    # assert chain_metadata.ipfs == compiled_metadata.ipfs, "IPFS hash mismatch"
    # assert chain_metadata.solc == compiled_metadata.solc, "SOLC version mismatch"

def test_bytecode_cgrt_token_compare_chain_and_compiled_shanghai_0_8_18():
    chain_bytecode = Bytecode(pathlib.Path("tests/utils/resources/bytecode/cgpt_token/chain.bytecode").open().read())
    chain_metadata = chain_bytecode.metadata

    compiled_bytecode = Bytecode(
        pathlib.Path("tests/utils/resources/bytecode/cgpt_token/compiled-shanghai-0.8.18.bytecode").open().read()
    )
    compiled_metadata = compiled_bytecode.metadata

    assert chain_bytecode.contract_hash == compiled_bytecode.contract_hash, "Contract hash mismatch"
    # assert chain_metadata.ipfs == compiled_metadata.ipfs, "IPFS hash mismatch"
    assert chain_metadata.solc == compiled_metadata.solc, "SOLC version mismatch"
