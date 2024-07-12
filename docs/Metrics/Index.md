# Metrics

## Health check

- [Health check](Healthcheck.md)

## Components

- [Collector](Collector.md)
- [Registry](Registry.md)
- [Metrics Server](MetricsServer.md)

## Metrics

- [Counter Metric](Counter.md)
- [Gauge Metric](Gauge.md)
- [Summary](Summary.md)
- [Histogram](Histogram.md)
- [Info](Info.md)
- [Enum](Enum.md)

## Metrics Configuration

| Parameter            | Type    | Default | Description                                                                                    |
| -------------------- | ------- | ------- | ---------------------------------------------------------------------------------------------- |
| `monitoring_enabled` | BOOLEAN | False   | A boolean which specifies if the telemetry will be enabled                                     |
| `monitoring_port`    | INTEGER | 9090    | A telemetry port for consuming metrics via MetricServer sentry, if `monitoring_enabled` = True |


