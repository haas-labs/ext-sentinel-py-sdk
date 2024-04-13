# Based on https://github.com/claws/aioprometheus

from typing import Union, cast

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType

CounterValueType = Union[int, float]


class Counter(Collector):
    kind = MetricsTypes.counter

    def get(self, labels: LabelsType) -> CounterValueType:
        """Get the Counter value matching an arbitrary group of labels.

        :raises: KeyError if an item with matching labels is not present.
        """
        return self.get_value(labels)

    def set(self, labels: LabelsType, value: CounterValueType) -> None:
        """Set the counter to an arbitrary value."""
        self.set_value(labels, value)

    def inc(self, labels: LabelsType) -> None:
        """Increments the counter by 1."""
        self.add(labels, 1)

    def add(self, labels: LabelsType, value: CounterValueType) -> None:
        """Add the given value to the counter.

        :raises: ValueError if the value is negative. Counters can only
          increase.
        """
        value = cast(Union[float, int], value)  # typing check, no runtime behaviour.
        if value < 0:
            raise ValueError("Counters can't decrease")

        try:
            current = self.get_value(labels)
        except KeyError:
            current = 0

        current = cast(Union[float, int], current)  # typing check, no runtime behaviour.
        self.set_value(labels, current + value)
