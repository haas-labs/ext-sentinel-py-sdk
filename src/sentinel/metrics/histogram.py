# Based on https://github.com/claws/aioprometheus and refactored


from collections import OrderedDict
from typing import cast, List, Dict, Union, Optional, Sequence

from sentinel.metrics.collector import Collector
from sentinel.metrics.types import MetricsTypes, BucketType, LabelsType

HistogramValueTypes = Union[int, float]

POS_INF = float("+Inf")
NEG_INF = float("-Inf")


def linearBuckets(start: Union[float, int], width: Union[int, float], count: int) -> List[BucketType]:
    """
    Returns buckets that are spaced linearly.

    Returns ``count`` buckets, each ``width`` wide, where the lowest bucket
    has an upper bound of ``start``. There is no +Inf bucket is included in
    the returned list.

    :raises: Exception if ``count`` is zero or negative.
    """
    if count < 1:
        raise Exception("Invalid count, must be a positive number")
    return [start + i * width for i in range(count)]


def exponentialBuckets(start: Union[float, int], factor: Union[float, int], count: int) -> List[BucketType]:
    """
    Returns buckets that are spaced exponentially.

    Returns ``count`` buckets, where the lowest bucket has an upper bound of
    ``start`` and each following bucket's upper bound is ``factor`` times the
    previous bucket's upper bound. There is no +Inf bucket is included in the
    returned list.

    :raises: Exception if ``count`` is 0 or negative.
    :raises: Exception if ``start`` is 0 or negative,
    :raises: Exception if ``factor`` is less than or equal 1.
    """

    if count < 1:
        raise Exception("Invalid count, must be a positive number")
    if start <= 0:
        raise Exception("Invalid start, must be positive")
    if factor < 1:
        raise Exception("Invalid factor, must be greater than one")
    return [start * (factor**i) for i in range(count)]


class Histogram(Collector):
    kind = MetricsTypes.histogram

    REPR_STR = "histogram"
    DEFAULT_BUCKETS = (
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
        POS_INF,
    )
    SUM_KEY = "sum"
    COUNT_KEY = "count"

    def __init__(
        self,
        name: str,
        doc: str,
        labels: Optional[LabelsType] = None,
        # registry: Optional["Registry"] = None,
        buckets: Sequence[float] = DEFAULT_BUCKETS,
    ) -> None:
        super().__init__(name, doc, labels=labels)
        self.upper_bounds = buckets

    def add(self, value: HistogramValueTypes, labels: LabelsType = None) -> None:
        """Add a single observation to the histogram"""

        value = cast(Union[float, int], value)  # typing check, no runtime behaviour.
        if type(value) not in (float, int):
            raise TypeError("Histogram only works with digits (int, float)")

        try:
            h = self.get_value(labels=labels)
            h = cast(HistogramStruct, h)  # typing check, no runtime behaviour.
        except KeyError:
            # Initialize histogram aggregator
            h = HistogramStruct(*self.upper_bounds)
            self.set_value(labels=labels, value=h)

        h.observe(value=float(value))

    # https://prometheus.io/docs/instrumenting/writing_clientlibs/#histogram
    # A histogram MUST have the ``observe`` methods
    observe = add

    def get(self, labels: LabelsType = None) -> Dict[Union[float, str], HistogramValueTypes]:
        """
        Get a dict of values, containing the sum, count and buckets,
        matching an arbitrary group of labels.

        :raises: KeyError if an item with matching labels is not present.
        """
        return_data = OrderedDict()  # type: Dict[Union[float, str], HistogramValueTypes]

        h = self.get_value(labels=labels)
        h = cast(HistogramStruct, h)  # typing check, no runtime behaviour.

        for upper_bound, cumulative_count in h.buckets.items():
            return_data[upper_bound] = cumulative_count  # keys are floats

        # Set sum and count
        return_data[self.COUNT_KEY] = h.observations
        return_data[self.SUM_KEY] = h.sum

        return return_data

    def dump_values(self) -> List[HistogramValueTypes]:
        return [{"labels": labels, "values": dict(values)} for labels, values in self.get_all()]


class HistogramStruct:
    """
    A Histogram counts individual observations from an event into configurable
    buckets. This histogram implementation also provides a sum and count of
    observations.
    """

    def __init__(self, *buckets: BucketType) -> None:
        _buckets = [float(b) for b in buckets]

        if _buckets != sorted(buckets):
            raise ValueError("Buckets not in sorted order")

        if _buckets and _buckets[-1] != POS_INF:
            _buckets.append(POS_INF)

        if len(_buckets) < 2:
            raise ValueError("Must have at least two buckets")

        self.buckets = OrderedDict([(b, 0) for b in _buckets])  # type: Dict[float, int]
        self.observations = 0  # type: int
        self.sum = 0.0  # type: float

    def observe(self, value: Union[float, int]) -> None:
        """
        Observe the given amount.

        Observing a value into the histogram will cumulatively increment the
        count of observations for the buckets that the observed values falls
        within. It also adds the value to the sum of all observations.

        :param value: A metric value to add to the histogram.
        """
        for upper_bound in self.buckets:
            if value <= upper_bound:
                self.buckets[upper_bound] += 1
        self.sum += value
        self.observations += 1
