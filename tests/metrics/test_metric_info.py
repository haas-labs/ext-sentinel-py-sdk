import time

from sentinel.metrics.info import Info
from sentinel.metrics.types import MetricsTypes

DEFAULT_DATA = {
    "name": "component_info",
    "doc": "Information about component",
    "labels": {"component": "comp_a"},
}


def test_metric_info_init():
    i = Info(**DEFAULT_DATA)
    assert i.name == DEFAULT_DATA["name"], "Incorrect info metric name"
    assert i.doc == DEFAULT_DATA["doc"], "Incorrect info metric doc"
    assert i.labels == DEFAULT_DATA["labels"], "Incorrect info metric labels"


def test_metric_info_set_and_get():
    i = Info(**DEFAULT_DATA)
    labels = {"component": "comp_b"}
    COMP_B_DATA = {"version": "0.1.0", "build_time": "2024-04-13 12:34:00"}
    i.set(labels=labels, value=COMP_B_DATA)

    info_details = i.get(labels=labels)
    assert info_details["version"] == COMP_B_DATA["version"], "Incorrect component version"
    assert info_details["build_time"] == COMP_B_DATA["build_time"], "Incorrect component build time"


def test_metric_info_dump():
    i = Info(**DEFAULT_DATA)
    labels = {"component": "comp_b"}
    COMP_B_DATA = {"version": "0.1.0", "build_time": "2024-04-13 12:34:00"}
    i.set(labels=labels, value=COMP_B_DATA)

    expected_data = [{"labels": labels, "values": COMP_B_DATA}]

    timestamp = int(time.time() * 1000)
    metrics_dump = i.dump()
    assert metrics_dump.kind == MetricsTypes.info.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp >= timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of counter data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
