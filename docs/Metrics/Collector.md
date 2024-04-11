# Metric Collector

## Metric names and labels

Every time series is uniquely identified by its metric name and a set of key-value pairs, also known as labels.

Labels enable Prometheus's dimensional data model: any given combination of labels for the same metric name identifies a particular dimensional instantiation of that metric (for example: all HTTP requests that used the method POST to the /api/tracks handler). The query language allows filtering and aggregation based on these dimensions. Changing any label value, including adding or removing a label, will create a new time series.

Label names may contain ASCII letters, numbers, as well as underscores. They must match the regex ``[a-zA-Z_][a-zA-Z0-9_]*``. Label names beginning with ``__`` are reserved for internal use.

## Samples

Samples form the actual time series data. Each sample consists of:

- a float64 value
- a millisecond-precision timestamp

## Notation

Given a metric name and a set of labels, time series are frequently identified using this notation:

```
<metric name>{<label name>=<label value>, ...}
```

For example, a time series with the metric name
`api_http_requests_total` and the labels `method="POST"` and `handler="/messages"` could be written like this:
```
api_http_requests_total{method="POST", handler="/messages"}
```
