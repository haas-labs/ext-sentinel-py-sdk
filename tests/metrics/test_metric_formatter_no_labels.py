from metric_samples import get_sample

from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.core import MetricDatabase
from sentinel.metrics.formatter import PrometheusFormattter


def test_metric_formatter_format_enum_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.stateset, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_enum_metric Test Enum Metric",
            "# TYPE test_enum_metric stateset",
            'test_enum_metric{"module":"A"} running ' + f"{ts}",
            "",
        ]
    ), "Incorrect enum text format w/o root labels"


def test_metric_formatter_format_enum_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.stateset, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_enum_metric Test Enum Metric",
            "# TYPE test_enum_metric stateset",
            'test_enum_metric{"component":"A"} running ' + f"{ts}",
            "",
        ]
    ), "Incorrect enum text format w/o value labels"


def test_metric_formatter_format_enum_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.stateset, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_enum_metric Test Enum Metric",
            "# TYPE test_enum_metric stateset",
            "test_enum_metric running " + f"{ts}",
            "",
        ]
    ), "Incorrect enum text format w/o labels"


def test_metric_formatter_format_info_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.info, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_info_metric Test Info Metric",
            "# TYPE test_info_metric info",
            'test_info_metric_version{"module":"A"} 0.1.0 ' + f"{ts}",
            'test_info_metric_build_time{"module":"A"} 2024-04-13T12:34:00 ' + f"{ts}",
            "",
        ]
    ), "Incorrect info text format w/o root labels"


def test_metric_formatter_format_info_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.info, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_info_metric Test Info Metric",
            "# TYPE test_info_metric info",
            'test_info_metric_version{"component":"A"} 0.1.0 ' + f"{ts}",
            'test_info_metric_build_time{"component":"A"} 2024-04-13T12:34:00 ' + f"{ts}",
            "",
        ]
    ), "Incorrect info text format w/o value labels"


def test_metric_formatter_format_info_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.info, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_info_metric Test Info Metric",
            "# TYPE test_info_metric info",
            "test_info_metric_version 0.1.0 " + f"{ts}",
            "test_info_metric_build_time 2024-04-13T12:34:00 " + f"{ts}",
            "",
        ]
    ), "Incorrect info text format w/o labels"


def test_metric_formatter_format_counter_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_counter_metric Test Counter Metric",
            "# TYPE test_counter_metric counter",
            'test_counter_metric{"module":"A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format w/o root labels"


def test_metric_formatter_format_counter_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_counter_metric Test Counter Metric",
            "# TYPE test_counter_metric counter",
            'test_counter_metric{"component":"A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format w/o value labels"


def test_metric_formatter_format_counter_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.counter, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_counter_metric Test Counter Metric",
            "# TYPE test_counter_metric counter",
            "test_counter_metric 10 " + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format w/o labels"


def test_metric_formatter_format_gauge_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.gauge, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_gauge_metric Test Gauge Metric",
            "# TYPE test_gauge_metric gauge",
            'test_gauge_metric{"module":"A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect gauge text format w/o root labels"


def test_metric_formatter_format_gauge_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.gauge, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_gauge_metric Test Gauge Metric",
            "# TYPE test_gauge_metric gauge",
            'test_gauge_metric{"component":"A"} 10 ' + f"{ts}",
            "",
        ]
    ), "Incorrect gauge text format w/o value labels"


def test_metric_formatter_format_gauge_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.gauge, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_gauge_metric Test Gauge Metric",
            "# TYPE test_gauge_metric gauge",
            "test_gauge_metric 10 " + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format w/o labels"


def test_metric_formatter_format_summary_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.summary, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_summary_metric Test Summary Metric",
            "# TYPE test_summary_metric summary",
            'test_summary_metric_count{"module":"A"} 4 ' + f"{ts}",
            'test_summary_metric_sum{"module":"A"} 25.2 ' + f"{ts}",
            'test_summary_metric_avg{"module":"A"} 6.3 ' + f"{ts}",
            'test_summary_metric_quantile{"module":"A","quantile":0.5} 4.6 ' + f"{ts}",
            'test_summary_metric_quantile{"module":"A","quantile":0.9} 10.66 ' + f"{ts}",
            'test_summary_metric_quantile{"module":"A","quantile":0.99} 12.766 ' + f"{ts}",
            "",
        ]
    ), "Incorrect summary text format w/o root labels"


def test_metric_formatter_format_summary_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.summary, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_summary_metric Test Summary Metric",
            "# TYPE test_summary_metric summary",
            'test_summary_metric_count{"component":"A"} 4 ' + f"{ts}",
            'test_summary_metric_sum{"component":"A"} 25.2 ' + f"{ts}",
            'test_summary_metric_avg{"component":"A"} 6.3 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","quantile":0.5} 4.6 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","quantile":0.9} 10.66 ' + f"{ts}",
            'test_summary_metric_quantile{"component":"A","quantile":0.99} 12.766 ' + f"{ts}",
            "",
        ]
    ), "Incorrect summary text format w/o value labels"


def test_metric_formatter_format_summary_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.summary, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_summary_metric Test Summary Metric",
            "# TYPE test_summary_metric summary",
            "test_summary_metric_count 4 " + f"{ts}",
            "test_summary_metric_sum 25.2 " + f"{ts}",
            "test_summary_metric_avg 6.3 " + f"{ts}",
            'test_summary_metric_quantile{"quantile":0.5} 4.6 ' + f"{ts}",
            'test_summary_metric_quantile{"quantile":0.9} 10.66 ' + f"{ts}",
            'test_summary_metric_quantile{"quantile":0.99} 12.766 ' + f"{ts}",
            "",
        ]
    ), "Incorrect summary text format w/o labels"


def test_metric_formatter_format_histogram_no_root_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.histogram, current_time=True)
    metric.labels = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_histogram_metric Test Histogram Metric",
            "# TYPE test_histogram_metric histogram",
            'test_histogram_metric_bucket{"module":"A","le":"0.005"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.01"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.025"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.05"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.1"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.25"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"0.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"1.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"2.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"5.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"module":"A","le":"10.0"} 2 ' + f"{ts}",
            'test_histogram_metric_inf{"module":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_count{"module":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_sum{"module":"A"} +Inf ' + f"{ts}",
            "",
        ]
    ), "Incorrect histogram text format w/o root labels"


def test_metric_formatter_format_histogram_no_value_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.histogram, current_time=True)
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_histogram_metric Test Histogram Metric",
            "# TYPE test_histogram_metric histogram",
            'test_histogram_metric_bucket{"component":"A","le":"0.005"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.01"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.025"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.05"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.1"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.25"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"0.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"1.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"2.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"5.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"component":"A","le":"10.0"} 2 ' + f"{ts}",
            'test_histogram_metric_inf{"component":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_count{"component":"A"} 3 ' + f"{ts}",
            'test_histogram_metric_sum{"component":"A"} +Inf ' + f"{ts}",
            "",
        ]
    ), "Incorrect histogram text format w/o value labels"


def test_metric_formatter_format_histogram_no_labels():
    db = MetricDatabase()

    metric = get_sample(kind=MetricsTypes.histogram, current_time=True)
    metric.labels = None
    metric.values[0]["labels"] = None
    ts = metric.timestamp
    db.update(metric)
    formatter = PrometheusFormattter()
    lines = formatter.format(db)
    assert lines == "\n".join(
        [
            "# HELP test_histogram_metric Test Histogram Metric",
            "# TYPE test_histogram_metric histogram",
            'test_histogram_metric_bucket{"le":"0.005"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.01"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.025"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.05"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.1"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.25"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"0.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"1.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"2.5"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"5.0"} 0 ' + f"{ts}",
            'test_histogram_metric_bucket{"le":"10.0"} 2 ' + f"{ts}",
            'test_histogram_metric_inf 3 ' + f"{ts}",
            'test_histogram_metric_count 3 ' + f"{ts}",
            'test_histogram_metric_sum +Inf ' + f"{ts}",
            "",
        ]
    ), "Incorrect counter text format w/o labels"
