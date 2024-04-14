import time

from sentinel.metrics.gauge import Gauge
from sentinel.metrics.types import MetricsTypes

DEFAULT_DATA = {
    "name": "hdd_disk_used",
    "doc": "Disk space used",
    "labels": {"server": "1.db.production.my-app"},
}


def test_metric_gauge_init():
    g = Gauge(**DEFAULT_DATA)

    assert g.name == DEFAULT_DATA["name"], "Incorrect gauge metric name"
    assert g.doc == DEFAULT_DATA["doc"], "Incorrect gauge metric doc"
    assert g.labels == DEFAULT_DATA["labels"], "Incorrect gauge metric labels"

    # TODO check metrics automatically got registered
    # collector_name = self.default_data["name"]
    # self.assertIn(collector_name, REGISTRY.collectors)


def test_metric_gauge_set_and_get():
    g = Gauge(**DEFAULT_DATA)
    data = (
        {"labels": {"max": "500G", "dev": "sda"}, "values": range(0, 500, 50)},
        {"labels": {"max": "1T", "dev": "sdb"}, "values": range(0, 1000, 100)},
        {"labels": {"max": "10T", "dev": "sdc"}, "values": range(0, 10000, 1000)},
    )
    for i in data:
        for j in i["values"]:
            g.set(i["labels"], j)
            assert g.get(i["labels"]) == j, "Incorrect metric value"

    assert len(data) == len(g.values), "Incorrect gauge metric values"


def test_metric_gauge_without_labels():
    g = Gauge(**DEFAULT_DATA)
    data = {"labels": {}, "values": range(100)}

    for i in data["values"]:
        g.set(data["labels"], i)

    assert len(g.values) == 1, "Incorrect gauge metric values"
    assert max(data["values"]) == g.get(data["labels"]), "Incorrect gauge metric values"


def test_metric_gauge_inc():
    g = Gauge(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    iterations = 100

    for i in range(iterations):
        g.inc(labels)
        assert g.get(labels) == i + 1, "Incorrect gauge metric value after inc"

    assert g.get(labels) == iterations, "Incorrect gauge metric value after all inc"


def test_metric_gauge_dec():
    g = Gauge(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    iterations = 100
    g.set(labels, iterations)

    for i in range(iterations):
        g.dec(labels)
        assert g.get(labels) == iterations - (i + 1), "Incorrect gauge metric value after inc"

    assert g.get(labels) == 0, "Incorrect gauge metric value after all dec"


def test_metric_gauge_add():
    g = Gauge(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    iterations = 100

    for i in range(iterations):
        g.add(labels, i)

    assert g.get(labels) == sum(range(iterations)), "Incorrect gauge metric value"

    for i in range(iterations):
        g.add(labels, -i)

    assert g.get(labels) == 0, "Incorrect gauge metric value"


def test_metric_gauge_sub():
    g = Gauge(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    iterations = 100

    for i in range(iterations):
        g.sub(labels, -i)

    assert g.get(labels) == sum(range(iterations)), "Incorrect gauge metric value"

    for i in range(iterations):
        g.sub(labels, i)

    assert g.get(labels) == 0, "Incorrect gauge metric value"


def test_metric_gauge_dump_all():
    g = Gauge(**DEFAULT_DATA)
    labels = {"max": "10T", "dev": "sdc"}
    iterations = 100

    for i in range(iterations):
        g.inc(labels)

    expected_data = ({"labels": labels, "values": 100},)

    timestamp = int(time.time() * 1000)
    metrics_dump = g.dump()
    assert metrics_dump.kind == MetricsTypes.gauge.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp >= timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of counter data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
