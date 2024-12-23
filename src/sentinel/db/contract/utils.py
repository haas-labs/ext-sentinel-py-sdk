from typing import Dict, List

from hexbytes import HexBytes
from web3 import Web3

from sentinel.models.contract import (
    ABIRecord,
    ABISignature,
)


def get_abi_input_types(abi: ABIRecord) -> List[str]:
    """
    returns ABI Input types
    """
    types = []
    for input in abi.inputs:
        if input.indexed:
            continue
        types.append(input.type)
    return types


def get_abi_input_fields(abi: Dict) -> Dict[str, str]:
    """
    returns ABI Input fields (w/o indexed)
    - field name
    - field type
    """
    fields = {}
    for input in abi.inputs:
        if input.indexed:
            continue
        fields[input.name] = input.type
    return fields


def extract_data_from_topics(abi_record: ABIRecord, topics: List[str]) -> Dict:
    """
    Extract data from topics
    """
    kv = {}
    if len(topics) == 0:
        return kv

    topics = topics.copy()
    kv["event_signature_hash"] = topics.pop(0)

    if len(topics) != 0:
        w3 = Web3()
        for input in abi_record.inputs:
            if input.indexed and len(topics) != 0:
                topic_data = HexBytes(topics.pop(0))
                kv[input.name] = w3.codec.decode(types=[input.type], data=topic_data)[0]
    return kv


def extract_data_from_event_log(abi_record: ABIRecord, topics: List[str], data: str) -> Dict:
    """
    Extract data from event
    """
    fields = {}

    w3 = Web3()
    data_fields = get_abi_input_fields(abi_record)
    types = list(data_fields.values())
    fields = extract_data_from_topics(abi_record, topics)
    if data != "0x":
        fields.update(dict(zip(data_fields, w3.codec.decode(types, HexBytes(data)))))

    return fields


def to_signature_record(contract_address: str, abi_record: ABIRecord) -> ABISignature:
    """
    Convert ABI Record to ABI Signature Record
    """
    types = [input.type for input in abi_record.inputs]
    signature = "{}({})".format(abi_record.name, ",".join(types))
    signature_hash = Web3.keccak(text=signature).hex()
    if not signature_hash.startswith("0x"):
        signature_hash = "0x{}".format(signature_hash)

    abi_signature = ABISignature(
        contract_address=contract_address,
        type=abi_record.type,
        signature_hash=signature_hash,
        signature=signature,
        abi=abi_record,
    )
    return abi_signature
