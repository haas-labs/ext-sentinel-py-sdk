from sentinel.metrics.info import Info

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
    i.set(labels, COMP_B_DATA)

    info_details = i.get(labels)
    assert info_details["version"] == COMP_B_DATA["version"], "Incorrect component version"
    assert info_details["build_time"] == COMP_B_DATA["build_time"], "Incorrect component build time"

