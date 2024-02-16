import pathlib

from sentinel.formats.jsonrpc import JsonRPCFormat
from sentinel.models.transaction import Transaction


def test_jsonrpc_format_read_transaction():
    """
    Test JSONRPC format read
    """
    jsrpc = JsonRPCFormat()
    assert isinstance(jsrpc, JsonRPCFormat), "Incorrect type format"

    path = pathlib.Path("tests/formats/resources/jsonrpc_transaction_extended_v2.jsonl")
    data = list(jsrpc.read(path=path, record_type=Transaction))

    assert len(data) == 1, f"Expected one transaction per file, detected: {len(data)}"
