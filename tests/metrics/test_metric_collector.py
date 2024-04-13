# Re-org from https://github.com/claws/aioprometheus

import time
import pytest

from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.collector import Collector

DEFAULT_DATA = {
    "name": "logged_users_total",
    "doc": "Logged users in the application",
    "labels": {"app": "my_app"},
}


def test_metric_collector_init():
    c = Collector(**DEFAULT_DATA)
    assert isinstance(c, Collector), "Incorrect collector type"
    assert c.name == DEFAULT_DATA["name"]
    assert c.doc == DEFAULT_DATA["doc"]
    assert c.labels == DEFAULT_DATA["labels"]

    # TODO check metrics automatically got registered
    # collector_name = self.default_data["name"]
    # self.assertIn(collector_name, REGISTRY.collectors)


def test_metrics_collector_invalid_metric_name():
    with pytest.raises(ValueError) as err:
        Collector(
            **{
                "name": "logged.users.total",
                "doc": "Logged users in the application",
            }
        )
    assert str(err.value) == "Invalid metric name: logged.users.total", "Incorrect exception text"


def test_metric_collector_set_and_get_values():
    c = Collector(**DEFAULT_DATA)

    data = (
        ({"country": "sp", "device": "desktop"}, 520),
        ({"country": "us", "device": "mobile"}, 654),
        ({"country": "uk", "device": "desktop"}, 1001),
        ({"country": "de", "device": "desktop"}, 995),
    )

    for m in data:
        c.set_value(m[0], m[1])

    assert len(data) == len(c.values), "Incorrect metrics data in collector"

    for m in data:
        assert c.get_value(m[0]) == m[1], "Incorrect metric value"


def test_metric_collector_set_same_values():
    c = Collector(**DEFAULT_DATA)
    data = (
        ({"country": "sp", "device": "desktop", "ts": "GMT+1"}, 520),
        ({"ts": "GMT+1", "country": "sp", "device": "desktop"}, 521),
        ({"country": "sp", "ts": "GMT+1", "device": "desktop"}, 522),
        ({"device": "desktop", "ts": "GMT+1", "country": "sp"}, 523),
    )
    for m in data:
        c.set_value(m[0], m[1])
    assert len(c.values) == 1, "Incorrect number of metrics"
    assert c.values[data[0][0]] == 523, "Incorrect metric value"


def test_metric_collector_missed_fields():
    data = DEFAULT_DATA.copy()
    del data["name"]
    with pytest.raises(TypeError) as err:
        Collector(**data)
    assert (
        str(err.value) == "Collector.__init__() missing 1 required positional argument: 'name'"
    ), "Incorrect error message"

    data = DEFAULT_DATA.copy()
    del data["doc"]
    with pytest.raises(TypeError) as err:
        Collector(**data)
    assert (
        str(err.value) == "Collector.__init__() missing 1 required positional argument: 'doc'"
    ), "Incorrect error message"

    data = DEFAULT_DATA.copy()
    del data["labels"]
    c = Collector(**data)
    assert isinstance(c, Collector), "Incorrect collector type"


def test_metric_collector_withot_labels():
    c = Collector(**DEFAULT_DATA)
    data = (({}, 520), (None, 654), ("", 1001))

    for i in data:
        c.set_value(i[0], i[1])

    assert len(c.values) == 1, "Incorrect number of values"
    assert c.values[data[0][0]] == 1001, "Incorrect metric's value"


def test_metric_collector_wrong_labels():
    c = Collector(**DEFAULT_DATA)

    # Normal set
    with pytest.raises(ValueError) as err:
        c.set_value({"job": 1, "ok": 2}, 1)

    assert str(err.value) == "Invalid label name: job", "Incorrect exception text"

    with pytest.raises(ValueError) as err:
        c.set_value({"__not_ok": 1, "ok": 2}, 1)

    assert str(err.value) == "Invalid label prefix: __not_ok", "Incorrect exception text"

    # Constructor set
    with pytest.raises(ValueError) as err:
        Collector("x", "y", {"job": 1, "ok": 2})

    assert str(err.value) == "Invalid label name: job", "Incorrect exception text"

    with pytest.raises(ValueError) as err:
        Collector("x", "y", {"__not_ok": 1, "ok": 2})

    assert str(err.value) == "Invalid label prefix: __not_ok", "Incorrect exception text"


def test_metric_collector_check_all():
    c = Collector(**DEFAULT_DATA)
    data = (
        ({"country": "sp", "device": "desktop"}, 520),
        ({"country": "us", "device": "mobile"}, 654),
        ({"country": "uk", "device": "desktop"}, 1001),
        ({"country": "de", "device": "desktop"}, 995),
        ({"country": "zh", "device": "desktop"}, 520),
        ({"country": "ch", "device": "mobile"}, 654),
        ({"country": "ca", "device": "desktop"}, 1001),
        ({"country": "jp", "device": "desktop"}, 995),
        ({"country": "au", "device": "desktop"}, 520),
        ({"country": "py", "device": "mobile"}, 654),
        ({"country": "ar", "device": "desktop"}, 1001),
        ({"country": "pt", "device": "desktop"}, 995),
    )
    for i in data:
        c.set_value(i[0], i[1])

    def country_fetcher(x):
        return x[0]["country"]

    sorted_data = sorted(data, key=country_fetcher)
    sorted_result = sorted(c.get_all(), key=country_fetcher)
    assert sorted_data == sorted_result, "Incorrect data comparison for get_all()"


def test_metric_collector_dump_all():
    c = Collector(**DEFAULT_DATA)
    data = (
        ({"country": "sp", "device": "desktop"}, 520),
        ({"country": "us", "device": "mobile"}, 654),
        ({"country": "uk", "device": "desktop"}, 1001),
    )
    expected_data = (
        {"labels": {"country": "sp", "device": "desktop"}, "values": 520},
        {"labels": {"country": "us", "device": "mobile"}, "values": 654},
        {"labels": {"country": "uk", "device": "desktop"}, "values": 1001},
    )

    for i in data:
        c.set_value(i[0], i[1])

    timestamp = int(time.time() * 1000)
    metrics_dump = c.dump()
    assert metrics_dump.kind == MetricsTypes.untyped.value, "Incorrect collector type"
    assert metrics_dump.name == DEFAULT_DATA["name"], "Incorrect collector name"
    assert metrics_dump.doc == DEFAULT_DATA["doc"], "Incorrect collector doc"
    assert metrics_dump.labels == DEFAULT_DATA["labels"], "Incorrect collector labels"
    assert metrics_dump.timestamp >= timestamp, "Incorrect collector data timestamp"

    assert len(metrics_dump.values) == len(expected_data), "Incorrect number of collector data records"
    for i, record in enumerate(metrics_dump.values):
        assert expected_data[i] == record, "Incorrect record"
