# re-org from https://github.com/claws/aioprometheus

import pytest
from sentinel.metrics.metricdict import MetricDict


def test_metricdict_init():
    metrics = MetricDict()
    assert isinstance(metrics, MetricDict), "Incorrect metrics type"


def test_metricdict_incorrect_key():
    metrics = MetricDict()
    with pytest.raises(TypeError):
        metrics["not_valid"] = "value"


def test_metricdict_empty_key():
    metrics = MetricDict()
    metrics[None] = 100

    assert metrics[None] == 100
    assert metrics[""] == 100
    assert metrics[{}] == 100


def test_metricdict_access_by_str_key():
    metrics = MetricDict()
    value = 100

    label = {"b": 2, "c": 3, "a": 1}
    metrics[label] = 100

    # Wrong string
    with pytest.raises(TypeError) as err:
        metrics["dasdasd"]
    assert str(err.value) == "Only accepts dicts as keys"

    # Access ok with string
    access_key = b'{"a":1,"b":2,"c":3}'
    assert metrics[access_key] == value

    # Access ok but wrong key by order
    with pytest.raises(KeyError) as err:
        bad_access_key = b'{"b": 2, "c": 3, "a": 1}'
        metrics[bad_access_key]
    assert err.value.args[0] == bad_access_key, "Access by wrong key"


def test_metricdict_set_and_get():
    metrics = MetricDict()
    data = (
        ({"a": 1}, 1000),
        ({"b": 2, "c": 3}, 2000),
        ({"d": 4, "e": 5, "f": 6}, 3000),
    )

    for i in data:
        metrics[i[0]] = i[1]

    assert len(data) == len(metrics), "Incorrect data"
    for i in data:
        assert i[1] == metrics[i[0]]

    assert [m for m in metrics] == [b'{"a":1}', b'{"b":2,"c":3}', b'{"d":4,"e":5,"f":6}'], "Incorrect metrics values"


def test_metricdict_delete():
    metrics = MetricDict()

    data = (
        ({"d": 4, "e": 5, "f": 6}, 3000),
        ({"e": 5, "d": 4, "f": 6}, 4000),
        ({"d": 4, "f": 6, "e": 5}, 5000),
        ({"d": 41, "f": 61, "e": 51}, 6000),
        ({"d": 41, "e": 51, "f": 61}, 7000),
        ({"f": 61, "e": 51, "d": 41}, 8000),
    )

    for i in data:
        metrics[i[0]] = i[1]

    del metrics[i[0]]

    assert len(metrics) == 1, "Incorrect data"
