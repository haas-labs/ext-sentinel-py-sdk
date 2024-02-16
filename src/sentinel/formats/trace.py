from dataclasses import dataclass
from collections import defaultdict

from typing import Dict, List, Optional


@dataclass
class AddressMetrics:
    from_counter: int = 0
    to_counter: int = 0


class Trace:
    """
    Trace
    """

    def __init__(self, data: Dict) -> None:
        """
        Trace Init
        """
        self.data: Dict = data

    def extract(self, types: Optional[List[str]]):
        """
        extract trace records

        by types - extract records with specific type(-s) only
        """
        if self.data.get("calls", []):
            for record in self._flatten(self.data.get("calls")):
                if types and record.get("type", "") not in types:
                    continue
                yield record

    def stats_by_address(self, types: Optional[List[str]]) -> Dict[str, AddressMetrics]:
        """
        Trace stats by addresses
        """
        stats = defaultdict(AddressMetrics)
        for record in self.extract(types=types):
            stats[record.get("from")].from_counter += 1
            stats[record.get("to")].to_counter += 1
        return dict(stats)

    def _flatten(self, calls: List):
        """
        Flat trace records
        """
        for call in calls:
            call_record = call.copy()
            if call.get("calls", []):
                for call_record_in in self._flatten(call.get("calls")):
                    yield call_record_in
                call_record.pop("calls")
            yield call_record
