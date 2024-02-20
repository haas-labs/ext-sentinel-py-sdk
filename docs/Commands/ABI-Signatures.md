# ABI Signatures Command

```sh
sentinel abi-signatures --help
usage: sentinel abi-signatures [-h] [-l LOG_LEVEL] [--rich-logging] [--env-vars ENV_VARS] --from CONTRACT_LIST --to TO [--skip-existing]

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  --rich-logging        Activate rich logging
  --env-vars ENV_VARS   Set environment variables from JSON/YAML file
  --from CONTRACT_LIST  The contract list, CSV file with address and network
  --to TO               Store ABI signatures in the directory
  --skip-existing       Skip existing contract(-s)
```
