# Based on https://github.com/claws/aioprometheus

from typing import cast, Union

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType

GaugeValueType = Union[int, float]


class Gauge(Collector):
    kind = MetricsTypes.gauge

    def set(self, labels: LabelsType, value: GaugeValueType) -> None:
        """Set the gauge to an arbitrary value."""
        self.set_value(labels, value)

    def get(self, labels: LabelsType) -> GaugeValueType:
        """Get the gauge value matching an arbitrary group of labels.

        :raises: KeyError if an item with matching labels is not present.
        """
        return self.get_value(labels)

    def inc(self, labels: LabelsType) -> None:
        """Increments the gauge by 1."""
        self.add(labels, 1)

    def dec(self, labels: LabelsType) -> None:
        """Decrement the gauge by 1."""
        self.add(labels, -1)

    def add(self, labels: LabelsType, value: GaugeValueType) -> None:
        """Add the given value to the Gauge.

        The value can be negative, resulting in a decrease of the gauge.
        """
        value = cast(Union[float, int], value)  # typing check, no runtime behaviour.

        try:
            current = self.get_value(labels)
        except KeyError:
            current = 0
        current = cast(Union[float, int], current)  # typing check, no runtime behaviour.

        self.set_value(labels, current + value)

    def sub(self, labels: LabelsType, value: GaugeValueType) -> None:
        """Subtract the given value from the Gauge.

        The value can be negative, resulting in an increase of the gauge.
        """
        value = cast(Union[float, int], value)  # typing check, no runtime behaviour.
        self.add(labels, -value)
