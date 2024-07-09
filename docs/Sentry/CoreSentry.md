# Core Sentry

`sentinel.core.v2.sentry.CoreSentry`

The processing unit, used for building new Sentry types like Transaction and Transaction Block Detectors, or for
building simple unit for one run processing. There are not inputs and outputs, but databases can be attached.

## Parameters

- name: Sentry name
- description: Sentry Description
- restart: the flag for a dispatcher, indicate if a sentry should be restarted, by default: true
- parameters: Sentry parameters from configuration
- schedule: the cron-like string with scheduler details
- settings: Sentry settings, see `models.Sentry`

## Methods

- `from_settings`: create sentry instance based on settings
- `run`: the main method for running a sentry
- `init`: init method for initialization logger and database(-s)
- `time_to_run`: the method returns run dates: previous, current, next

## Events handlers

Sentry calls these handlers on different stages of execution

- `on_init`: Sentry calls it after initialization process - init()
- `on_schedule`: used in case when you need to execute certain logic by scheduler
- `on_run`: User-defined processing logic 
