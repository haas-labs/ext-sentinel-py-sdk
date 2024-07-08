# Async Core Sentry

`sentinel.core.v2.sentry.AsyncCoreSentry`

Async Core Senty, based on [[CoreSentry]]. The main difference compare to Core Sentry, the Async Core Sentry 
has asynchronious nature. Supports:
- Async inputs and outputs 
- monitoring logic

The processing logic must be async as well

## Methods

- `from_settings`: additionally to CoreSentry.from_settings there are 2 new parameters for monitoring configuration
  - `monitoring_enabled`: boolean flag - true/false
  - `monitoring_port`: the port number for publishing metrics via Metrics Server, by default: 9090

## Properties

- `metrics`: returns Metrics Registry

## Event handlers

- `on_init`: Sentry calls it after initialization process - init()

