import multiprocessing
import time
from typing import Any, Dict, Iterator, List

from pydantic import BaseModel, Field
from sentinel.metrics.collector import MetricModel


class MetricQueue:
    def __init__(self):
        self._metrics_queue = multiprocessing.Queue()

    def send(self, metrics: MetricModel) -> None:
        self._metrics_queue.put(metrics)

    def receive(self) -> MetricModel:
        return self._metrics_queue.get()

    @property
    def size(self) -> int:
        return self._metrics_queue.qsize()


class MetricDBRecord(BaseModel):
    kind: int
    name: str
    doc: str
    labels: Dict[str, str] = Field(default_factory=list)
    timestamp: int
    values: Any


class MetricDatabase:
    """
    Metric Database, used in Metric Server for metrics publishing
    """

    def __init__(self, retention_period: int = 30) -> None:
        """
        :param retention_period: time interval in seconds for removing outdated records,
                                 default: 30 secs
        """
        self._metrics: List[MetricDBRecord] = list()
        self.retention_period = retention_period * 1000

    @property
    def size(self):
        return len(self._metrics)

    def all(self) -> Iterator[MetricDBRecord]:
        current_time = int(time.time() * 1000)
        for metric in self._metrics:
            if (current_time - metric.timestamp) >= self.retention_period:
                continue
            yield metric

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
            self._metrics.append(metric_record)

    def clean(self) -> None:
        """
        Remove outdated metrics
        """
        metrics = [m for m in self._metrics if (int(time.time() * 1000) - m.timestamp) <= self.retention_period]
        self._metrics = metrics
