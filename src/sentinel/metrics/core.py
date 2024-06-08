import hashlib
import time
from typing import Any, Dict, Iterator

from pydantic import BaseModel, Field
from sentinel.metrics.collector import MetricModel


class MetricDBRecord(BaseModel):
    kind: int
    name: str
    doc: str
    labels: Dict[str, str] = Field(default_factory=dict)
    timestamp: int
    values: Any

    @property
    def hash(self) -> int:
        _key = f"{self.kind}{self.name}{self.doc}{sorted(self.labels.items())}".encode("utf-8")
        return hashlib.sha256(_key).hexdigest()


class MetricDatabase:
    """
    Metric Database, used in Metric Server for metrics publishing
    """

    def __init__(self, retention_period: int = 60) -> None:
        """
        :param retention_period: time interval in seconds for removing outdated records,
                                 default: 60 secs
        """
        self._metrics: Dict[str, MetricDBRecord] = dict()
        self.retention_period = retention_period * 1000

    @property
    def size(self):
        return len(self._metrics)

    def current_time(self) -> int:
        return int(time.time() * 1000)

    def all(self) -> Iterator[MetricDBRecord]:
        current_time = int(time.time() * 1000)
        for metric in self._metrics.values():
            if (current_time - metric.timestamp) >= self.retention_period:
                continue
            yield metric.model_copy()

    def update(self, metric: MetricModel) -> None:
        for v in metric.values:
            labels = metric.labels.copy() if isinstance(metric.labels, dict) else {}
            value_labels = v.pop("labels", {})
            if isinstance(value_labels, dict):
                labels.update(value_labels)
            metric_record = MetricDBRecord(
                kind=metric.kind,
                name=metric.name,
                doc=metric.doc,
                labels=labels,
                values=v.get("values"),
                timestamp=metric.timestamp,
            )
            self._metrics[metric_record.hash] = metric_record

    def clean(self) -> None:
        """
        Remove outdated metrics
        """
        current_time = self.current_time()
        metrics = {k: m for k, m in self._metrics.items() if (current_time - m.timestamp) <= self.retention_period}
        self._metrics = metrics
