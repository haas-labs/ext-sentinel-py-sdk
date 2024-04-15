from typing import Dict

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType

InfoValueType = Dict[str, str]


class Info(Collector):
    kind = MetricsTypes.info

    def get(self, labels: LabelsType = None) -> InfoValueType:
        """
        Get info metric value
        """
        return self.get_value(labels)

    def set(self, value: InfoValueType, labels: LabelsType = None) -> None:
        """Set info metric value"""
        self.set_value(labels, value)
