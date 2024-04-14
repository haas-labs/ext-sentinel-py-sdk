import pytest

from sentinel.metrics.core import MetricQueue
from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.collector import MetricModel

from sentinel.metrics.enum import Enum
from sentinel.metrics.info import Info
from sentinel.metrics.gauge import Gauge
from sentinel.metrics.counter import Counter
from sentinel.metrics.summary import Summary
from sentinel.metrics.histogram import Histogram, POS_INF


def test_metric_queue_init():
    metrics = MetricQueue()
    assert isinstance(metrics, MetricQueue), "Incorrect metric queue type"


@pytest.mark.asyncio
async def test_metric_queue_send_receive():
    TEST_METRICS = {"total_requests": 10}
    metric_queue = MetricQueue()
    await metric_queue.send(metrics=TEST_METRICS)
    metrics = await metric_queue.receive()
    assert metrics == TEST_METRICS, "Unexpected metric value"


@pytest.mark.asyncio
async def test_metric_queue_send_receive_enum():
    metric_queue = MetricQueue()
    e = Enum(
        name="test_enum_metric",
        doc="Test Enum Metric",
        labels={
            "component": "A",
        },
        states=["not_started", "running", "finished"],
    )
    e.set(labels={"module": "A"}, value="running")

    await metric_queue.send(metrics=e.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.stateset.value, "Incorrect metric kind"
    assert metrics.name == "test_enum_metric", "Unexpected metric name"
    assert metrics.doc == "Test Enum Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [{"labels": {"module": "A"}, "values": "running"}], "Unexpected metric values"

@pytest.mark.asyncio
async def test_metric_queue_send_receive_info():
    metric_queue = MetricQueue()
    i = Info(
        name="test_info_metric",
        doc="Test Info Metric",
        labels={
            "component": "A",
        },
    )
    i.set(labels={"module": "A"}, value={"version": "0.1.0", "build_time": "2024-04-13 12:34:00"})

    await metric_queue.send(metrics=i.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.info.value, "Incorrect metric kind"
    assert metrics.name == "test_info_metric", "Unexpected metric name"
    assert metrics.doc == "Test Info Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [
        {"labels": {"module": "A"}, "values": {"version": "0.1.0", "build_time": "2024-04-13 12:34:00"}}
    ], "Unexpected metric values"


@pytest.mark.asyncio
async def test_metric_queue_send_receive_gauge():
    metric_queue = MetricQueue()
    g = Gauge(
        name="test_gauge_metric",
        doc="Test Gauge Metric",
        labels={
            "component": "A",
        },
    )
    g.add(labels={"module": "A"}, value=10)

    await metric_queue.send(metrics=g.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.gauge.value, "Incorrect metric kind"
    assert metrics.name == "test_gauge_metric", "Unexpected metric name"
    assert metrics.doc == "Test Gauge Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [{"labels": {"module": "A"}, "values": 10}], "Unexpected metric values"


@pytest.mark.asyncio
async def test_metric_queue_send_receive_counter():
    metric_queue = MetricQueue()
    c = Counter(
        name="test_counter_metric",
        doc="Test Counter Metric",
        labels={
            "component": "A",
        },
    )
    c.add(labels={"module": "A"}, value=10)

    await metric_queue.send(metrics=c.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.counter.value, "Incorrect metric kind"
    assert metrics.name == "test_counter_metric", "Unexpected metric name"
    assert metrics.doc == "Test Counter Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [{"labels": {"module": "A"}, "values": 10}], "Unexpected metric values"


@pytest.mark.asyncio
async def test_metric_queue_send_receive_summary():
    metric_queue = MetricQueue()
    s = Summary(
        name="test_summary_metric",
        doc="Test Summary Metric",
        labels={
            "component": "A",
        },
    )
    s.add(labels={"module": "A"}, value=3)
    s.add(labels={"module": "A"}, value=5.2)
    s.add(labels={"module": "A"}, value=4)
    s.add(labels={"module": "A"}, value=13)

    await metric_queue.send(metrics=s.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.summary.value, "Incorrect metric kind"
    assert metrics.name == "test_summary_metric", "Unexpected metric name"
    assert metrics.doc == "Test Summary Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [
        {
            "labels": {"module": "A"},
            "values": {
                "count": 4,
                "sum": 25.2,
                "avg": 6.3,
                "quantile": [
                    {"quantile": 0.5, "value": 4.6},
                    {"quantile": 0.9, "value": 10.66},
                    {"quantile": 0.99, "value": 12.766},
                ],
            },
        }
    ], "Unexpected metric values"


@pytest.mark.asyncio
async def test_metric_queue_send_receive_histogram():
    metric_queue = MetricQueue()
    h = Histogram(
        name="test_histogram_metric",
        doc="Test Histogram Metric",
        labels={
            "component": "A",
        },
    )
    h.observe(labels={"module": "A"}, value=7)
    h.observe(labels={"module": "A"}, value=7.5)
    h.observe(labels={"module": "A"}, value=POS_INF)

    await metric_queue.send(metrics=h.dump())
    metrics: MetricModel = await metric_queue.receive()

    assert metrics.kind == MetricsTypes.histogram.value, "Incorrect metric kind"
    assert metrics.name == "test_histogram_metric", "Unexpected metric name"
    assert metrics.doc == "Test Histogram Metric", "Unexpected metric doc"
    assert metrics.labels == {"component": "A"}, "Unexpected metric labels"
    assert metrics.values == [
        {
            "labels": {"module": "A"},
            "values": {
                0.005: 0,
                0.01: 0,
                0.025: 0,
                0.05: 0,
                0.1: 0,
                0.25: 0,
                0.5: 0,
                1.0: 0,
                2.5: 0,
                5.0: 0,
                10.0: 2,
                POS_INF: 3,
                "count": 3,
                "sum": POS_INF,
            },
        }
    ], "Unexpected metric values"
