from typing import Dict, Iterator, List

from sentinel.db.contract.utils import extract_data_from_event_log
from sentinel.models.contract import ABISignature
from sentinel.models.transaction import LogEntry


def filter_log_entries(log_entries: List[LogEntry], signatures: List[ABISignature]) -> Iterator[Dict]:
    """
    Filter Transaction Log Entries by the list of required ABI Signatures

    For example:

    for event in filter_events(transaction.logs, [ABI_EVENT_TRANSFER]):
        ...
    """
    for log_entry in log_entries:
        if len(log_entry.topics) == 0:
            continue

        signature_hash = log_entry.topics[0]
        for signature in signatures:
            if signature_hash == signature.signature_hash:
                if log_entry.data == "0x":
                    continue
                event: Dict = extract_data_from_event_log(
                    abi_record=signature.abi,
                    topics=log_entry.topics,
                    data=log_entry.data,
                )
                event["type"] = signature.abi.name
                yield event
