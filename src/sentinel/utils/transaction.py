from dataclasses import dataclass
from typing import Dict, Iterator, List

from sentinel.db.contract.utils import extract_data_from_event_log
from sentinel.models.contract import ABISignature
from sentinel.models.transaction import LogEntry


@dataclass
class Event:
    address: str
    type: str
    fields: Dict[str, str]


def filter_events(log_entries: List[LogEntry], signatures: List[ABISignature]) -> Iterator[Event]:
    for log_entry in log_entries:
        if len(log_entry.topics) == 0:
            continue

        signature_hash = log_entry.topics[0]
        for signature in signatures:
            if signature_hash == signature.signature_hash:
                yield Event(
                    address=log_entry.address.lower(),
                    type=signature.abi.name,
                    fields=extract_data_from_event_log(
                        abi_record=signature.abi,
                        topics=log_entry.topics,
                        data=log_entry.data,
                    ),
                )
