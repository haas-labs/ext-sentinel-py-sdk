import time
import pytest

from sentinel.metrics.counter import Counter
from sentinel.metrics.types import MetricsTypes

DEFAULT_DATA = {
    "name": "logged_users_total",
    "doc": "Logged users in the application",
    "labels": {"app": "my_app"},
}


def test_metric_counter_init():
    c = Counter(**DEFAULT_DATA)
    assert isinstance(c, Counter), "Incorrect counter type"
    assert c.name == "logged_users_total", "Incorrect counter name"
    assert c.doc == "Logged users in the application", "Incorrect counter doc"
    assert c.labels == {"app": "my_app"}, "Incorrect counter labels"

    # TODO check metrics automatically got registered
    # collector_name = self.default_data["name"]
    # self.assertIn(collector_name, REGISTRY.collectors)


def test_metric_counter_set_and_get():
    c = Counter(**DEFAULT_DATA)
    data = (
        {"labels": {"country": "sp", "device": "desktop"}, "values": range(10)},
        {"labels": {"country": "us", "device": "mobile"}, "values": range(10, 20)},
        {"labels": {"country": "uk", "device": "desktop"}, "values": range(20, 30)},
    )

    for i in data:
        for j in i["values"]:
            c.set(i["labels"], j)
            assert c.get(i["labels"]) == j, "Incorrect metric value"

    assert len(data) == len(c.values), "Incorrect counter metric values"

    # Last check
    for i in data:
        assert max(i["values"]) == c.get(i["labels"]), "Incorrect counter value"


def test_metric_counter_get_no_labels():
    c = Counter(**DEFAULT_DATA)
    data = {"labels": {}, "values": range(100)}

    for i in data["values"]:
        c.set(data["labels"], i)

    assert len(c.values) == 1, "Incorrect number of counter metrics"
    assert max(data["values"]) == c.get(data["labels"]), "Incorrect counter metric values"


def test_metric_counter_inc():
    c = Counter(**DEFAULT_DATA)
    iterations = 100
    labels = {"country": "sp", "device": "desktop"}

    for i in range(iterations):
        c.inc(labels)

    assert c.get(labels) == iterations, "Incorrect counter metric value"


def test_metric_counter_add():
    c = Counter(**DEFAULT_DATA)
    iterations = 100
    labels = {"country": "sp", "device": "desktop"}

    for i in range(iterations):
        c.add(labels, i)

    assert c.get(labels) == sum(range(iterations)), "Incorrect counter metric value"


def test_metric_counter_negative_add():
    c = Counter(**DEFAULT_DATA)
    labels = {"country": "sp", "device": "desktop"}

    with pytest.raises(ValueError) as err:
        c.add(labels, -1)

    assert str(err.value) == "Counters can't decrease", "Incorrect behavior, counter can't descrease"


def test_metric_counter_dump_all():
    c = Counter(**DEFAULT_DATA)
    data = (
        {"labels": {"country": "sp", "device": "desktop"}, "values": range(10)},
        {"labels": {"country": "us", "device": "mobile"}, "values": range(10, 20)},
        {"labels": {"country": "uk", "device": "desktop"}, "values": range(20, 30)},
    )
    expected_data = (
        {"labels": {"country": "sp", "device": "desktop"}, "values": 9},
        {"labels": {"country": "us", "device": "mobile"}, "values": 19},
        {"labels": {"country": "uk", "device": "desktop"}, "values": 29},
    )

    for i in data:
        for j in i["values"]:
            c.set(i["labels"], j)

    timestamp = int(time.time() * 1000)
    metrics_dump = c.dump()
    assert metrics_dump.kind == MetricsTypes.counter.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp == timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of counter data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
