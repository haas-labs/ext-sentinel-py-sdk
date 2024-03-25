# Inventory

```sh
$ sentinel inventory --help
usage: sentinel inventory

Sentinel Inventory

options:
  -h, --help            show this help message and exit
  --scan PATH           Search components in the path
  --type TYPE           Component type, supported: project, sentry, input, output, database
  --env-vars ENV_VARS   Set environment variables from JSON/YAML file

global options:
  -L LEVEL, --log-level LEVEL
                        log level (default: INFO)
  --rich-logging        Activate rich logging
```