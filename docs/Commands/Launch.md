# Launch Command

```sh
sentinel launch --help
usage: sentinel launch [-h] [-l LOG_LEVEL] [--rich-logging] --profile PROFILE [--import-service-tokens] [--vars VARS] [--env-vars ENV_VARS]

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  --rich-logging        Activate rich logging
  --profile PROFILE     Sentinel Process Profile
  --import-service-tokens
                        Import service tokens before launch
  --vars VARS           Set additional variables as JSON, if filename prepend with @. Support YAML/JSON file
  --env-vars ENV_VARS   Set environment variables from JSON/YAML file
```
