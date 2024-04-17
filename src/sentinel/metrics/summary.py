# Based on https://github.com/claws/aioprometheus and refactored

import statistics
from collections import deque
from dataclasses import dataclass
from typing import cast, Optional, Dict, Union

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, LabelsType


SummaryValueType = Union[int, float]


@dataclass
class SummaryMetric:
    sum: float
    count: int
    values: deque


class Summary(Collector):
    kind = MetricsTypes.summary

    def __init__(
        self,
        name: str,
        doc: str,
        labels: Optional[LabelsType] = None,
        # registry: Optional["Registry"] = None,
        max_values: int = 1_000,
    ) -> None:
        """
        :param max_values: max values in metric for analysis
        """
        # super().__init__(name, doc, const_labels=const_labels, registry=registry)
        super().__init__(name, doc, labels=labels)
        self.max_values = max_values

    def add(self, value: SummaryValueType, labels: LabelsType = None) -> None:
        """Add a single observation to the summary"""

        value = cast(Union[float, int], value)  # typing check, no runtime behaviour.
        if type(value) not in (float, int):
            raise TypeError("Summary only works with digits (int, float)")

        try:
            metric: SummaryMetric = self.get_value(labels=labels)
        except KeyError:
            # Initialize metric
            metric = SummaryMetric(sum=0.0, count=0, values=deque(maxlen=self.max_values))

        metric.count += 1
        metric.sum += value
        metric.values.append(value)
        self.set_value(labels=labels, value=metric)

    # https://prometheus.io/docs/instrumenting/writing_clientlibs/#summary
    # A summary MUST have the ``observe`` methods
    observe = add

    def get(self, labels: LabelsType = None) -> Dict[Union[float, str], SummaryValueType]:
        """
        Get a dict of values, containing the sum, count and quantiles,
        matching an arbitrary group of labels.

        :raises: KeyError if an item with matching labels is not present.
        """
        return_data = dict()

        metric: SummaryMetric = self.get_value(labels=labels)

        data = list(metric.values)
        return_data["count"] = metric.count
        return_data["sum"] = metric.sum
        return_data["avg"] = return_data["sum"] / return_data["count"]
        quantiles = statistics.quantiles(data, n=100, method="inclusive") if data else []
        return_data["quantile"] = [
            {"quantile": 0.5, "value": round(quantiles[49], 4)},
            {"quantile": 0.9, "value": round(quantiles[89], 4)},
            {"quantile": 0.99, "value": round(quantiles[98], 4)},
        ]
        return return_data
