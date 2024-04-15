import json
from typing import Dict, List

from sentinel.metrics.types import MetricsTypes
from sentinel.metrics.metricdict import MetricDict
from sentinel.metrics.histogram import POS_INF, NEG_INF
from sentinel.metrics.core import MetricDatabase, MetricDBRecord

HELP_FMT = "# HELP {name} {doc}"
TYPE_FMT = "# TYPE {name} {kind}"
COMMENT_FMT = "# {comment}"
LINE_SEPARATOR_FMT = "\n"


class PrometheusFormattter:
    """
    Prometheus Metric Formatter

    This formatter encodes into the Text (Prometheus) format.

    The histogram and summary types are difficult to represent in the text
    format. The following conventions apply:

      - The sample sum for a summary or histogram named x is given as a
        separate sample named x_sum.
      - The sample count for a summary or histogram named x is given as a
        separate sample named x_count.
      - Each quantile of a summary named x is given as a separate sample line
        with the same name x and a label {quantile="y"}.
      - Each bucket count of a histogram named x is given as a separate sample
        line with the name x_bucket and a label {le="y"} (where y is the upper
        bound of the bucket).
      - A histogram must have a bucket with {le="+Inf"}. Its value must be
        identical to the value of x_count.
      - The buckets of a histogram and the quantiles of a summary must appear
        in increasing numerical order of their label values (for the le or
        the quantile label, respectively).
    """

    def group_metrics(self, db: MetricDatabase) -> Dict:
        """
        Group metrics by kind, metric name and use just latest values
        """
        groups = dict()
        for metric in db.all():
            if metric.kind not in groups:
                groups[metric.kind] = dict()

            if metric.name not in groups[metric.kind]:
                groups[metric.kind][metric.name] = {"doc": metric.doc, "metrics": MetricDict()}

            groups[metric.kind][metric.name]["doc"] = metric.doc

            if metric.labels not in groups[metric.kind][metric.name]["metrics"]:
                groups[metric.kind][metric.name]["metrics"][metric.labels] = {
                    "values": metric.values,
                    "timestamp": metric.timestamp,
                }

            elif metric.timestamp > groups[metric.kind][metric.name]["metrics"][metric.labels]["timestamp"]:
                groups[metric.kind][metric.name]["metrics"][metric.labels] = {
                    "values": metric.values,
                    "timestamp": metric.timestamp,
                }

        return groups

    def format(self, db: MetricDatabase) -> str:
        """
        Format metrics into a bytes object
        """
        lines = []
        for metric in db.all():
            lines.extend(self.format_metric(metric))

        return LINE_SEPARATOR_FMT.join(lines).encode("utf-8")

    def format_metric(self, metric: MetricDBRecord) -> List[str]:
        """
        Format metric into a bytes object
        """
        # create headers
        help_header = HELP_FMT.format(name=metric.name, doc=metric.doc)
        type_header = TYPE_FMT.format(name=metric.name, kind=MetricsTypes(metric.kind).name)

        lines = [help_header, type_header]

        match metric.kind:
            case MetricsTypes.stateset.value:
                metric.labels = self.prep_labels(metric.labels)
                lines.extend(self.format_enum(metric))
            case MetricsTypes.info.value:
                metric.labels = self.prep_labels(metric.labels)
                lines.extend(self.format_info(metric))
            case MetricsTypes.counter.value:
                metric.labels = self.prep_labels(metric.labels)
                lines.extend(self.format_counter(metric))
            case MetricsTypes.gauge.value:
                metric.labels = self.prep_labels(metric.labels)
                lines.extend(self.format_gauge(metric))
            case MetricsTypes.summary.value:
                lines.extend(self.format_summary(metric))
            case MetricsTypes.histogram.value:
                lines.extend(self.format_histogram(metric))
            case _:
                raise ValueError(f"Unknown metric type, {metric.kind}")

        lines.append("")
        return lines

    def prep_labels(self, labels: Dict) -> str:
        return json.dumps(labels, separators=(",", ":"))

    def format_enum(self, metric: MetricDBRecord) -> List[str]:
        return [f"{metric.name}{metric.labels} {metric.values} {metric.timestamp}"]

    def format_info(self, metric: MetricDBRecord) -> List[str]:
        lines = []
        for k, v in metric.values.items():
            lines.append(f"{metric.name}_{k}{metric.labels} {v} {metric.timestamp}")
        return lines

    def format_counter(self, metric: MetricDBRecord) -> List[str]:
        return [f"{metric.name}{metric.labels} {metric.values} {metric.timestamp}"]

    def format_gauge(self, metric: MetricDBRecord) -> List[str]:
        return [f"{metric.name}{metric.labels} {metric.values} {metric.timestamp}"]

    def format_summary(self, metric: MetricDBRecord) -> List[str]:
        lines = []
        for k, v in metric.values.items():
            if k == "quantile":
                for q in metric.values["quantile"]:
                    labels = metric.labels.copy()
                    labels["quantile"] = q["quantile"]
                    labels = self.prep_labels(labels)
                    lines.append(f"{metric.name}_{k}{labels} {q['value']} {metric.timestamp}")
                continue
            labels = self.prep_labels(metric.labels)
            lines.append(f"{metric.name}_{k}{labels} {v} {metric.timestamp}")
        return lines

    def format_histogram(self, metric: MetricDBRecord) -> List[str]:
        lines = []
        for k, v in metric.values.items():
            labels = metric.labels.copy()
            if k in ("sum", "count", POS_INF, NEG_INF):
                if v == POS_INF:
                    v = "+Inf"
                elif v == NEG_INF:
                    v = "-Inf"
                labels = self.prep_labels(labels)
                lines.append(f"{metric.name}_{k}{labels} {v} {metric.timestamp}")
            elif isinstance(k, float):
                labels["le"] = str(k)
                labels = self.prep_labels(labels)
                lines.append(f"{metric.name}_bucket{labels} {v} {metric.timestamp}")
        return lines
