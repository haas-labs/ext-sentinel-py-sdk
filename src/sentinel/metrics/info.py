from typing import Dict

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType

InfoValueType = Dict[str, str]

class Info(Collector):
    kind = MetricsTypes.info

    def get(self, labels: LabelsType) -> InfoValueType:
        """
        Get info metric value
        """
        return self.get_value(labels)

    def set(self, labels: LabelsType, value: InfoValueType) -> None:
        """Set info metric value"""
        self.set_value(labels, value)


