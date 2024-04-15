from metric_samples import get_sample

from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.core import MetricDatabase
from sentinel.metrics.formatter import PrometheusFormattter

def test_metric_formatter_format_enum_no_labels():
    db = MetricDatabase()

    counter_metric = get_sample(kind=MetricsTypes.stateset, current_time=True)
    counter_metric.labels = None
    ts = counter_metric.timestamp
    db.update(counter_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_enum_metric Test Enum Metric",
            "# TYPE test_enum_metric stateset",
            'test_enum_metric{"component":"A","module":"A"} running ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"


def test_metric_formatter_format_info():
    db = MetricDatabase()

    counter_metric = get_sample(kind=MetricsTypes.info, current_time=True)
    ts = counter_metric.timestamp
    db.update(counter_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_info_metric Test Info Metric",
            "# TYPE test_info_metric info",
            'test_info_metric_version{"component":"A","module":"A"} 0.1.0 ' + f"{ts}",
            'test_info_metric_build_time{"component":"A","module":"A"} 2024-04-13T12:34:00 ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"


def test_metric_formatter_format_counter():
    db = MetricDatabase()

    counter_metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    ts = counter_metric.timestamp
    db.update(counter_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_counter_metric Test Counter Metric",
            "# TYPE test_counter_metric counter",
            'test_counter_metric{"component":"A","module":"A"} 10 ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"


def test_metric_formatter_format_gauge():
    db = MetricDatabase()

    gauge_metric = get_sample(kind=MetricsTypes.gauge, current_time=True)
    ts = gauge_metric.timestamp
    db.update(gauge_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_gauge_metric Test Gauge Metric",
            "# TYPE test_gauge_metric gauge",
            'test_gauge_metric{"component":"A","module":"A"} 10 ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"


def test_metric_formatter_format_summary():
    db = MetricDatabase()

    summary_metric = get_sample(kind=MetricsTypes.summary, current_time=True)
    ts = summary_metric.timestamp
    db.update(summary_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_summary_metric Test Summary Metric",
            "# TYPE test_summary_metric summary",
            'test_summary_metric_count{"component":"A","module":"A"} 4 ' + f"{ts}",
            'test_summary_metric_sum{"component":"A","module":"A"} 25.2 ' + f"{ts}",
            'test_summary_metric_avg{"component":"A","module":"A"} 6.3 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","module":"A","quantile":0.5} 4.6 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","module":"A","quantile":0.9} 10.66 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","module":"A","quantile":0.99} 12.766 ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"


def test_metric_formatter_format_histogram():
    db = MetricDatabase()

    histogram_metric = get_sample(kind=MetricsTypes.histogram, current_time=True)
    ts = histogram_metric.timestamp
    db.update(histogram_metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_histogram_metric Test Histogram Metric",
            "# TYPE test_histogram_metric histogram",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.005"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.01"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.025"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.05"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.1"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.25"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"0.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"1.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"2.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"5.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","module":"A","le":"10.0"} 2 ' + f"{ts}",
            'test_histogram_metric_inf{"component":"A","module":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_count{"component":"A","module":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_sum{"component":"A","module":"A"} +Inf ' + f"{ts}",
            "",
        ]
    ).encode("utf-8"), "Incorrect counter text format"
