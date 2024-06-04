from sentinel.metrics.counter import Counter
from sentinel.metrics.info import Info
from sentinel.metrics.registry import Registry


def test_metric_registry_info_use_cases():
    metrics = Registry()
    metrics.register(
        Info(
            name="detector_metadata",
            doc="Detector information/metadata",
        )
    )
    metrics.detector_metadata.set(
        labels={
            "detector": "test-detector",
        },
        value={"version": "0.1.0", "host": "127.0.0.1"},
    )

    assert metrics.detector_metadata.get({"detector": "test-detector"}) == {
        "host": "127.0.0.1",
        "version": "0.1.0",
    }, "Incorrect collector list"

    print(list(metrics.dump_all()))

    # assert list(registry.get("detector_metadata").dump_values()) == [], "Incorrect detector metadata"
    # assert list(registry.dump_all()) == [], "Incorrect metric values"
    # assert list(registry.dump_all()) == [], "Incorrect metric values"

    # registry.get("detector_metadata").set_value(
    #     labels={
    #         "detector": "test-detector",
    #     },
    #     value={"version": "0.1.0", "host": "127.0.0.1"},
    # )
    # print(list(registry.dump_all()))

    # assert False


def test_metric_registry_counter_use_cases():
    metrics = Registry()

    metrics.register(
        Counter(
            name="total_transactions",
            doc="Total transactions",
        )
    )
    metrics.total_transactions.inc(labels={"type": "incoming"})
    metrics.total_transactions.add(labels={"type": "incoming"}, value=10)
    print(list(metrics.dump_all()))

    metrics.total_transactions.add(labels={"type": "incoming"}, value=10)
    print(list(metrics.dump_all()))

    # assert False
