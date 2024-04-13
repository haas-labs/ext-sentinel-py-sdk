import time
import pytest

from sentinel.metrics.summary import Summary
from sentinel.metrics.types import MetricsTypes

DEFAULT_DATA = {
    "name": "http_request_duration_microseconds",
    "doc": "Request duration per application",
    "labels": {"app": "my_app"},
}


def test_metric_summary_init():
    s = Summary(**DEFAULT_DATA)
    assert s.name == DEFAULT_DATA["name"], "Incorrect metric name"
    assert s.doc == DEFAULT_DATA["doc"], "Incorrect metirc doc"
    assert s.labels == DEFAULT_DATA["labels"], "Incorrect metric labels"

    # TODO check metrics automatically got registered
    # collector_name = self.default_data["name"]
    # self.assertIn(collector_name, REGISTRY.collectors)


def test_metric_summary_add():
    s = Summary(**DEFAULT_DATA)
    data = (
        {"labels": {"handler": "/static"}, "values": range(0, 500, 50)},
        {"labels": {"handler": "/p"}, "values": range(0, 1000, 100)},
        {"labels": {"handler": "/p/login"}, "values": range(0, 10000, 1000)},
    )

    for i in data:
        for j in i["values"]:
            s.add(i["labels"], j)

    for i in data:
        assert s.values[i["labels"]].count == len(i["values"]), "Incorrect summary metric values"


def test_metric_summary_get():
    s = Summary(**DEFAULT_DATA)
    labels = {"handler": "/static"}
    values = [3, 5.2, 4, 13]

    for i in values:
        s.add(labels, i)

    data = s.get(labels)
    expected_data = {
        "sum": 25.2,
        "count": 4,
        "avg": 6.3,
        "quantile": [
            {"quantile": 0.5, "value": 4.6},
            {"quantile": 0.9, "value": 10.66},
            {"quantile": 0.99, "value": 12.766},
        ],
    }

    assert data == expected_data, "Incorrect summary metrics data"

    labels = None
    values = [3, 5.2, 13, 4]

    for i in values:
        s.add(labels, i)

    assert len(s.values) == 2, "Incorrect list of values"
    assert s.get(labels) == expected_data, "Incorrect summary metrics data"


def test_metric_summary_wrong_types():
    s = Summary(**DEFAULT_DATA)
    labels = None
    values = ["3", (1, 2), {"1": 2}, True]
    for i in values:
        with pytest.raises(TypeError) as err:
            s.add(labels, i)
        assert str(err.value) == "Summary only works with digits (int, float)", "Incorrect error message"


def test_metric_summary_dump():
    s = Summary(**DEFAULT_DATA)
    labels = {"handler": "/static"}
    values = [3, 5.2, 4, 13]

    for i in values:
        s.add(labels, i)

    expected_data = [
        {
            "labels": labels,
            "values": {
                "sum": 25.2,
                "count": 4,
                "avg": 6.3,
                "quantile": [
                    {"quantile": 0.5, "value": 4.6},
                    {"quantile": 0.9, "value": 10.66},
                    {"quantile": 0.99, "value": 12.766},
                ],
            },
        }
    ]

    timestamp = int(time.time() * 1000)
    metrics_dump = s.dump()
    assert metrics_dump.kind == MetricsTypes.summary.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp == timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of counter data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
