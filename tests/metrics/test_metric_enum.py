import time
import pytest

from sentinel.metrics.enum import Enum
from sentinel.metrics.types import MetricsTypes

DEFAULT_DATA = {
    "name": "component_state",
    "doc": "Current component state",
    "labels": {"component": "comp_a"},
    "states": ["not_started", "running", "finished"],
}


def test_metric_enum_init():
    e = Enum(**DEFAULT_DATA)
    assert e.name == DEFAULT_DATA["name"], "Incorrect metric name"
    assert e.doc == DEFAULT_DATA["doc"], "Incorrect metric doc"
    assert e.labels == DEFAULT_DATA["labels"], "Incorrect metric labels"
    assert e.states == DEFAULT_DATA["states"], "Incorrect metric states"


def test_metric_enum_missed_state():
    with pytest.raises(ValueError) as err:
        Enum(
            **{
                "name": "component_state",
                "doc": "Current component state",
                "labels": {"component": "comp_c"},
            }
        )
    assert str(err.value) == "No states provided for Enum metric: {name}".format(
        name="component_state"
    ), "Incorrect error message"


def test_metric_enum_set_and_get():
    e = Enum(**DEFAULT_DATA)
    labels = {"component": "comp_b"}

    e.set(labels=labels, value="running")
    assert e.get(labels) == "running", "Incorrect component B state"


def test_metric_enum_wrong_state():
    e = Enum(**DEFAULT_DATA)
    labels = {"component": "comp_d"}

    with pytest.raises(ValueError) as err:
        e.set(labels=labels, value="testing")
    assert str(err.value) == "Unknown state, testing", "Incorrect error message"


def test_metric_enum_dump_all():
    e = Enum(**DEFAULT_DATA)
    labels = {"component": "comp_b"}
    e.set(labels=labels, value="running")

    expected_data = (
        {"labels": labels, "values": "running"},
    )

    timestamp = int(time.time() * 1000)
    metrics_dump = e.dump()
    assert metrics_dump.kind == MetricsTypes.stateset.value, "Incorrect type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect labels"
    assert metrics_dump.timestamp >= timestamp, "Incorrect data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
