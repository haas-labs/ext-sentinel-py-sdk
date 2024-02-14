from sentinel.db.contract.utils import (
    get_abi_input_types,
    extract_data_from_topics,
    extract_data_from_event_log,
)

from sentinel.models.contract import ABIRecord


def test_get_abi_input_types_with_indexed():
    """
    Test Get ABI Input Types, With Indexed Input
    """
    abi = ABIRecord(
        **{
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "nullifierHash",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "relayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "fee",
                    "type": "uint256",
                },
            ],
            "name": "Withdrawal",
            "type": "event",
        }
    )
    assert get_abi_input_types(abi) == [
        "address",
        "bytes32",
        "uint256",
    ], "Incorrect types list"


def test_get_abi_input_types_without_indexed():
    """
    Test Get ABI Input Types, Without Indexed Input
    """
    abi = ABIRecord(
        **{
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "nullifierHash",
                    "type": "bytes32",
                },
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "relayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "fee",
                    "type": "uint256",
                },
            ],
            "name": "Withdrawal",
            "type": "event",
        }
    )
    assert get_abi_input_types(abi) == [
        "address",
        "bytes32",
        "address",
        "uint256",
    ], "Incorrect types list"


def test_extract_data_from_topics():
    """
    Test Extract Data From Topics
    """
    abi = ABIRecord(
        **{
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "nullifierHash",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "relayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "fee",
                    "type": "uint256",
                },
            ],
            "name": "Withdrawal",
            "type": "event",
        }
    )

    topics = [
        "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
        "0x000000000000000000000000a591b02d27c5957fa472b4d702f52f3001aa49d1",
    ]
    assert extract_data_from_topics(abi, topics) == {
        "event_signature_hash": "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
        "relayer": "0xa591b02d27c5957fa472b4d702f52f3001aa49d1",
    }, "Incorrect list of extracted fields"


def test_extract_date_from_event_log():
    """
    Test Extract Data from Event Log
    """
    abi = ABIRecord(
        **{
            "anonymous": False,
            "inputs": [
                {
                    "indexed": False,
                    "internalType": "address",
                    "name": "to",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "bytes32",
                    "name": "nullifierHash",
                    "type": "bytes32",
                },
                {
                    "indexed": True,
                    "internalType": "address",
                    "name": "relayer",
                    "type": "address",
                },
                {
                    "indexed": False,
                    "internalType": "uint256",
                    "name": "fee",
                    "type": "uint256",
                },
            ],
            "name": "Withdrawal",
            "type": "event",
        }
    )

    topics = [
        "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
        "0x000000000000000000000000a591b02d27c5957fa472b4d702f52f3001aa49d1",
    ]
    data = "0x000000000000000000000000a591b02d27c5957fa472b4d702f52f3001aa49d1131a48dffe430d128db78cb6fb80d2b08590536251da8baae08de93573db6d730000000000000000000000000000000000000000000000000000000000000000"

    assert extract_data_from_event_log(abi, topics, data) == {
        "event_signature_hash": "0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931",
        "relayer": "0xa591b02d27c5957fa472b4d702f52f3001aa49d1",
        "to": "0xa591b02d27c5957fa472b4d702f52f3001aa49d1",
        "nullifierHash": bytes.fromhex(
            "131a48dffe430d128db78cb6fb80d2b08590536251da8baae08de93573db6d73"
        ),
        "fee": 0,
    }, "Incorrect event log data"
