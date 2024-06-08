from metric_samples import get_sample
from sentinel.metrics.core import MetricDatabase
from sentinel.metrics.formatter import PrometheusFormattter
from sentinel.metrics.types import MetricsTypes


def test_metric_formatter_init():
    formatter = PrometheusFormattter()
    assert isinstance(formatter, PrometheusFormattter), "Incorrect formatter type"


def test_metric_formatter_group_metrics():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    db.update(metric)

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    metric.timestamp += 10
    db.update(metric)

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    metric.timestamp += 10
    db.update(metric)

    last_ts = metric.timestamp

    formatter = PrometheusFormattter()
    metrics = formatter.group_metrics(db)
    assert (
        len(metrics[MetricsTypes.counter.value]["test_counter_metric"]["metrics"]) == 1
    ), "Incorrect number of metrics"

    for v in metrics[MetricsTypes.counter.value]["test_counter_metric"]["metrics"].values():
        assert v["timestamp"] == last_ts, "Incorrect metric timestamp"


def test_metric_formatter_format_enum():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.stateset, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_enum_metric Test Enum Metric",
            "# TYPE test_enum_metric stateset",
            'test_enum_metric{"component"="A","module"="A"} running ' + f"{ts}",
            "",
        ]
    ), "Incorrect enum text format"


def test_metric_formatter_format_info():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.info, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_info_metric Test Info Metric",
            "# TYPE test_info_metric info",
            'test_info_metric_version{"component"="A","module"="A"} 0.1.0 ' + f"{ts}",
            'test_info_metric_build_time{"component"="A","module"="A"} 2024-04-13T12:34:00 ' + f"{ts}",
            "",
        ]
    ), "Incorrect info text format"


def test_metric_formatter_format_counter():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_counter_metric Test Counter Metric",
            "# TYPE test_counter_metric counter",
            'test_counter_metric{"component"="A","module"="A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format"


def test_metric_formatter_format_gauge():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.gauge, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_gauge_metric Test Gauge Metric",
            "# TYPE test_gauge_metric gauge",
            'test_gauge_metric{"component"="A","module"="A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect gauge text format"


def test_metric_formatter_format_summary():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.summary, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_summary_metric Test Summary Metric",
            "# TYPE test_summary_metric summary",
            'test_summary_metric_count{"component"="A","module"="A"} 4 ' + f"{ts}",
            'test_summary_metric_sum{"component"="A","module"="A"} 25.2 ' + f"{ts}",
            'test_summary_metric_avg{"component"="A","module"="A"} 6.3 ' + f"{ts}",
            'test_summary_metric_quantile{"component"="A","module"="A","quantile"=0.5} 4.6 ' + f"{ts}",
            'test_summary_metric_quantile{"component"="A","module"="A","quantile"=0.9} 10.66 ' + f"{ts}",
            'test_summary_metric_quantile{"component"="A","module"="A","quantile"=0.99} 12.766 ' + f"{ts}",
            "",
        ]
    ), "Incorrect summary text format"


def test_metric_formatter_format_histogram():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.histogram, current_time=True)
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_histogram_metric Test Histogram Metric",
            "# TYPE test_histogram_metric histogram",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.005"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.01"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.025"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.05"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.1"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.25"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="0.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="1.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="2.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="5.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component"="A","module"="A","le"="10.0"} 2 ' + f"{ts}",
            'test_histogram_metric_inf{"component"="A","module"="A"} 3 ' + f"{ts}",
            'test_histogram_metric_count{"component"="A","module"="A"} 3 ' + f"{ts}",
            'test_histogram_metric_sum{"component"="A","module"="A"} +Inf ' + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format"
