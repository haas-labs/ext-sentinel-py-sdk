# Based on https://github.com/claws/aioprometheus

import re
import json

from typing import Optional, List, Tuple

from sentinel.metrics.metricdict import MetricDict
# from sentinel.metrics.registry import Registry, get_registry
from sentinel.metrics.core import LabelsType, NumericValueType, MetricsTypes


METRIC_NAME_RE = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
RESTRICTED_LABELS_NAMES = ("job",)
RESTRICTED_LABELS_PREFIXES = ("__",)


class Collector:
    """
    Base class for all collectors.
    """

    kind = MetricsTypes.untyped

    def __init__(
        self,
        name: str,
        doc: str,
        labels: Optional[LabelsType] = None,
        # registry: Optional[Registry] = None,
    ) -> None:
        """
        :param name: The name of the metric.

        :param doc: A short description of the metric.

        :param const_labels: Labels that should always be included with all
          instances of this metric.

        :param registry: A collector registry that is responsible for
          rendering the metric into various formats. When a registry is
          not supplied then the metric will be registered with the default
          registry.
        """
        if not METRIC_NAME_RE.match(name):
            raise ValueError(f"Invalid metric name: {name}")
        self.name = name
        self.doc = doc

        if labels:
            self._check_labels(labels)
            self.labels = labels
        else:
            self.labels = {}

        self.values = MetricDict()

        # Register metric with a Registry or the default registry
        # if registry is None:
        #     registry = get_registry()
        # registry.register(self)

    def set_value(self, labels: LabelsType, value: NumericValueType) -> None:
        """Sets a value in the container"""
        if labels:
            self._check_labels(labels)
        self.values[labels] = value

    def get_value(self, labels: LabelsType) -> NumericValueType:
        """Gets a value in the container.

        :raises: KeyError if an item with matching labels is not present.
        """
        return self.values[labels]

    def get(self, labels: LabelsType) -> NumericValueType:
        """Gets a value in the container.

        Handy alias for `get_value`.

        :raises: KeyError if an item with matching labels is not present.
        """
        return self.get_value(labels)

    def _check_labels(self, labels: LabelsType) -> bool:
        """Check validity of label names.

        :raises: ValueError if labels are invalid
        """
        for k, _v in labels.items():
            # Check reserved labels
            if k in RESTRICTED_LABELS_NAMES:
                raise ValueError(f"Invalid label name: {k}")

            if self.kind == MetricsTypes.histogram:
                if k in ("le",):
                    raise ValueError(f"Invalid label name: {k}")

            # Check prefixes
            if any(k.startswith(i) for i in RESTRICTED_LABELS_PREFIXES):
                raise ValueError(f"Invalid label prefix: {k}")

        return True

    def get_all(self) -> List[Tuple[LabelsType, NumericValueType]]:
        """
        Returns a list populated with 2-tuples. The first element is
        a dict of labels and the second element is the value of the metric
        itself.
        """
        result = []
        for k in self.values:
            # Check if is a single value dict (custom empty key)
            key = (
                {} if k == MetricDict.EMPTY_KEY else json.loads(k)  # pylint: disable=no-member
            )
            result.append((key, self.get(k)))

        return result

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.doc == other.doc  # type: ignore
            and self.values == other.values  # type: ignore
        )
