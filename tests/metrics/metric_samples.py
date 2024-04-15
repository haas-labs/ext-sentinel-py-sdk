import time

from sentinel.metrics.histogram import POS_INF
from sentinel.metrics.collector import MetricModel, MetricsTypes


SAMPLE_ENUM_METRIC = MetricModel(
    kind=MetricsTypes.stateset,
    name="test_enum_metric",
    doc="Test Enum Metric",
    labels={"component": "A"},
    timestamp=1713106101629,
    values=[{"labels": {"module": "A"}, "values": "running"}],
)

SAMPLE_INFO_METRIC = MetricModel(
    kind=MetricsTypes.info,
    name="test_info_metric",
    doc="Test Info Metric",
    labels={"component": "A"},
    timestamp=1713106230960,
    values=[{"labels": {"module": "A"}, "values": {"version": "0.1.0", "build_time": "2024-04-13 12:34:00"}}],
)

SAMPLE_COUNTER_METRIC = MetricModel(
    kind=MetricsTypes.counter,
    name="test_counter_metric",
    doc="Test Counter Metric",
    labels={"component": "A"},
    timestamp=1713106301243,
    values=[{"labels": {"module": "A"}, "values": 10}],
)

SAMPLE_GAUGE_METRIC = MetricModel(
    kind=MetricsTypes.gauge,
    name="test_gauge_metric",
    doc="Test Gauge Metric",
    labels={"component": "A"},
    timestamp=1713106267583,
    values=[{"labels": {"module": "A"}, "values": 10}],
)

SAMPLE_SUMMARY_METRIC = MetricModel(
    kind=MetricsTypes.summary,
    name="test_summary_metric",
    doc="Test Summary Metric",
    labels={"component": "A"},
    timestamp=1713106330621,
    values=[
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
    ],
)

SAMPLE_HISTOGRAM_METRIC = MetricModel(
    kind=MetricsTypes.histogram,
    name="test_histogram_metric",
    doc="Test Histogram Metric",
    labels={"component": "A"},
    timestamp=1713106361187,
    values=[
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
    ],
)


def use_current_time(metric: MetricModel) -> MetricModel:
    _metric = metric.model_copy()
    _metric.timestamp = int(time.time() * 1000)
    return _metric
