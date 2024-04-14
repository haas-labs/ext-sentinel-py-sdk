# Re-org from https://github.com/claws/aioprometheus

import pytest

from sentinel.metrics.registry import Registry
from sentinel.metrics.collector import Collector

DEFAULT_DATA = {
    "name": "logged_users_total",
    "doc": "Logged users in the application",
    "labels": {"app": "my_app"},
}


def test_metrinc_registry_init():
    registry = Registry()
    assert isinstance(registry, Registry), "Incorrect registry type"


def test_metric_register_same_names():
    registry = Registry()
    registry.register(Collector(**DEFAULT_DATA))
    assert len(registry.collectors) == 1, "Incorrect number of collectors"

    with pytest.raises(ValueError) as err:
        registry.register(Collector(**DEFAULT_DATA))

    collector_name = DEFAULT_DATA["name"]
    assert str(err.value) == f"A collector for {collector_name} is already registered", "Incorrect error message"


def test_metric_register_wrong_type():
    registry = Registry()
    with pytest.raises(TypeError) as err:
        registry.register("Collector")
    assert str(err.value) == "Invalid collector type: Collector", "Incorrect error message"


def test_metric_registry_deregister():
    registry = Registry()

    registry.register(Collector(**DEFAULT_DATA))
    assert len(registry.collectors) == 1, "Incorrect number of collectors"

    registry.deregister(DEFAULT_DATA["name"])
    assert len(registry.collectors) == 0, "Incorrect number of collectors"


def test_metric_registry_get():
    registry = Registry()

    c = Collector(**DEFAULT_DATA)
    registry.register(c)
    assert registry.get(c.name) == c, "Incorrect collector"


def test_metric_registry_get_all_and_clear():
    registry = Registry()

    q = 100
    for i in range(q):
        registry.register(Collector("test" + str(i), "Test" + str(i)))

    result = list(registry.get_all())
    assert isinstance(result, list), "Incorrect type of returned value"
    assert len(result) == q, "Incorrect number of collectors in registry"

    registry.clear()
    result = list(registry.get_all())
    assert len(result) == 0, "Incorrect number of collectors in registry"

def test_metric_registry_dump():
    registry = Registry()
    q = 10
    expected_data = []
    for i in range(q):
        c = Collector("test" + str(i), "Test" + str(i))
        expected_data.append(c.dump())
        registry.register(c)
    
    for i, metric in enumerate(registry.dump_all()):
        assert metric.name == expected_data[i].name, "Incorrect expected metric dump (name)"
        assert metric.doc == expected_data[i].doc, "Incorrect expected metric dump (name)"
