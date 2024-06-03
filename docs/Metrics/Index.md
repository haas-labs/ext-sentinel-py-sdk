# Metrics

## Health check

- [Health check](/docs/Metrics/Healthcheck.md)

## Components

- [Collector](/docs/Metrics/Collector.md)
- [Registry](/docs/Metrics/Registry.md)
- [Metrics Channel]()
- [Metrics Server]()

## Metrics

- [Counter Metric](/docs/Metrics/Counter.md)
- [Gauge Metric](/docs/Metrics/Gauge.md)
- [Summary](/docs/Metrics/Summary.md)
- [Histogram](/docs/Metrics/Histogram.md)
- [Info](/docs/Metrics/Info.md)
- [Enum](/docs/Metrics/Enum.md)

## Project Config

### Monitoring Enabled

Default: False

A boolean which specifies if the telemetry will be enabled

### Monitoring Port

Default: 9090

A telemetry port for consuming metrics via MetricServer sentry, if TELEMETRY_ENABLED = True
