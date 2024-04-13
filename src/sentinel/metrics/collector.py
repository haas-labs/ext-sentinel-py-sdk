# Based on https://github.com/claws/aioprometheus

import re
import json
import time

from typing import Optional, List, Tuple, Dict, Union, Any

from sentinel.metrics.metricdict import MetricDict
from sentinel.metrics.types import LabelsType, MetricsTypes


from pydantic import BaseModel, Field


class MetricModel(BaseModel):
    kind: int
    name: str
    doc: str
    labels: Dict[str, str] = Field(default_factory=list)
    timestamp: int
    values: Any


NumericValueType = Union[int, float]

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
    ) -> None:
        """
        :param name: The name of the metric.

        :param doc: A short description of the metric.

        :param labels: Labels that should always be included with all
          instances of this metric.
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

    def dump_values(self) -> List[NumericValueType]:
        return [{"labels": labels, "values": values} for labels, values in self.get_all()]

    def dump(self) -> MetricModel:
        return MetricModel(
            kind=self.kind,
            name=self.name,
            doc=self.doc,
            labels=self.labels,
            timestamp=int(time.time() * 1000),
            values=self.dump_values(),
        )

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.doc == other.doc  # type: ignore
            and self.values == other.values  # type: ignore
        )
