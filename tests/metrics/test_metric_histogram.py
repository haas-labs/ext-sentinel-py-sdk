# Based on https://github.com/claws/aioprometheus and refactored

import time
import pytest

from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.histogram import Histogram, POS_INF

DEFAULT_DATA = {
    "name": "histogram_metric",
    "doc": "histogram doc",
    "labels": {"app": "my_app"},
    "buckets": [5.0, 10.0, 15.0],
}

EXPECTED_DATA = {
    "sum": 25.2,
    "count": 4,
    5.0: 2.0,
    10.0: 3.0,
    15.0: 4.0,
    POS_INF: 4.0,
}
INPUT_VALUES = [3, 5.2, 13, 4]


def test_metric_histogram_init():
    h = Histogram(**DEFAULT_DATA)
    assert h.name == DEFAULT_DATA["name"], "Incorrect histogram metric name"
    assert h.doc == DEFAULT_DATA["doc"], "Incorrect histogram metric doc"
    assert h.labels == DEFAULT_DATA["labels"], "Incorrect histogram metric labels"

    # TODO check metrics automatically got registered
    # collector_name = self.default_data["name"]
    # self.assertIn(collector_name, REGISTRY.collectors)


def test_metric_histogram_wrong_labels():
    h = Histogram(**DEFAULT_DATA)
    with pytest.raises(ValueError) as err:
        h.set_value({"le": 2}, 1)
    assert str(err.value) == "Invalid label name: le", "Incorrect error message"


def test_metric_histogram_insufficient_buckets():
    d = DEFAULT_DATA.copy()
    d["buckets"] = []
    h = Histogram(**d)
    # The underlying histogram object within the Histogram metric is
    # created when needing so any exception only occurs when an new
    # observation is performed.
    with pytest.raises(Exception) as err:
        h.observe(None, 3.0)
    assert str(err.value) == "Must have at least two buckets", "Incorrect error message"


def test_metric_histogram_unsorted_buckets():
    d = DEFAULT_DATA.copy()
    d["buckets"] = [10.0, 5.0]
    h = Histogram(**d)
    # The underlying histogram object within the Histogram metric is
    # created when needing so any exception only occurs when an new
    # observation is performed.
    with pytest.raises(Exception) as err:
        h.observe(None, 3.0)
    assert str(err.value) == "Buckets not in sorted order", "Incorrect error message"


def test_metric_histogram_expected_values():
    h = Histogram(**DEFAULT_DATA)
    labels = None

    h.observe(labels, 7)
    results = h.get(labels)
    assert results[5.0] == 0, "Incorrect historgram metric value"
    assert results[10.0] == 1, "Incorrect historgram metric value"
    assert results[15.0] == 1, "Incorrect historgram metric value"
    assert results[POS_INF] == 1, "Incorrect historgram metric value"
    assert results["count"] == 1, "Incorrect historgram metric value"
    assert results["sum"] == 7.0, "Incorrect historgram metric value"

    h.observe(labels, 7.5)
    results = h.get(labels)
    assert results[5.0] == 0, "Incorrect historgram metric value"
    assert results[10.0] == 2, "Incorrect historgram metric value"
    assert results[15.0] == 2, "Incorrect historgram metric value"
    assert results[POS_INF] == 2, "Incorrect historgram metric value"
    assert results["count"] == 2, "Incorrect historgram metric value"
    assert results["sum"] == 14.5, "Incorrect historgram metric value"

    h.observe(labels, POS_INF)
    results = h.get(labels)
    assert results[5.0] == 0, "Incorrect historgram metric value"
    assert results[10.0] == 2, "Incorrect historgram metric value"
    assert results[15.0] == 2, "Incorrect historgram metric value"
    assert results[POS_INF] == 3, "Incorrect historgram metric value"
    assert results["count"] == 3, "Incorrect historgram metric value"
    assert results["sum"] == POS_INF, "Incorrect historgram metric value"


def test_metric_histogram_get():
    h = Histogram(**DEFAULT_DATA)
    labels = {"path": "/"}
    for i in INPUT_VALUES:
        h.observe(labels, i)
    data = h.get(labels)
    assert data == EXPECTED_DATA, "Unexpected data"


def test_metric_histogram_add_get_without_labels():
    h = Histogram(**DEFAULT_DATA)
    labels = None
    for i in INPUT_VALUES:
        h.observe(labels, i)
    assert len(h.values) == 1, "Incorrect histogram metric data"
    assert h.get(labels) == EXPECTED_DATA, "Unexpected data"


def test_metric_histogram_dump_all():
    h = Histogram(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    h.observe(labels, 7)
    h.observe(labels, 7.5)
    h.observe(labels, POS_INF)

    expected_data = [{"labels": labels, "values": {5.0: 0, 10.0: 2, 15.0: 2, POS_INF: 3, "count": 3, "sum": POS_INF}}]

    timestamp = int(time.time() * 1000)
    metrics_dump = h.dump()
    assert metrics_dump.kind == MetricsTypes.histogram.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp == timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of counter data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
