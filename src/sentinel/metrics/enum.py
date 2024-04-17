from typing import Optional, Sequence

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType


class Enum(Collector):
    kind = MetricsTypes.stateset

    def __init__(
        self,
        name: str,
        doc: str,
        labels: Optional[LabelsType] = None,
        states: Optional[Sequence[str]] = None,
    ) -> None:
        super().__init__(name, doc, labels=labels)
        if not states:
            raise ValueError(f"No states provided for Enum metric: {name}")
        self.states = states

    def get(self, labels: LabelsType = None) -> str:
        """
        Get enum metric value
        """
        return self.states[self.get_value(labels)]

    def set(self, value: str, labels: LabelsType = None) -> None:
        """
        Set enum metric state.
        """
        if value not in self.states:
            raise ValueError(f"Unknown state, {value}")
        self.set_value(labels, self.states.index(value))
