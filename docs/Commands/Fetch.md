# Fetch Command

```sh
sentinel fetch --help
usage: sentinel fetch [-h] [-l LOG_LEVEL] [--rich-logging] --rpc RPC [--dataset {block,transaction,trace,trace_transaction,debug_trace_transaction}] --from-file FROM_FILE
                      [--to-file TO_FILE]

options:
  -h, --help            show this help message and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  --rich-logging        Activate rich logging
  --rpc RPC             JSON-RPC End-Point
  --dataset {block,transaction,trace,trace_transaction,debug_trace_transaction}
                        Dataset type for fetching
  --from-file FROM_FILE
                        Fetch data from list
  --to-file TO_FILE     Store results into file
```
