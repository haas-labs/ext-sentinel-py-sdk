# Simple Transaction Detector

__ATTENION__: If you run Detector not from detector directory, update `type` in __profile.yml__

Run Transaction detector against `Extractor` Ethereum ingest websocket proxy:

```bash
sentinel launch --profile profile-ws-extractor.yaml --rich-logging
```

Run Transaction detector with webscoket proxy endpoint in environment variable

```bash
export DEV_TRANSACTION_WS_URI=ws://proxy:9300

sentinel launch --profile profile-ws.yaml
```

Run Transaction detector with webscoket proxy endpoint in environment file

```bash
export DEV_TRANSACTION_WS_URI=ws://proxy:9300

sentinel launch --profile profile-ws.yaml --env-vars .envs/local.yml --rich-logging
```

Parameters:

- `profile`: the path to a detector profile
- `env-vars`: websocket configuration contains credentials, to avoid commiting sensitive information 
            in a profile, env-vars parameter helps easy import env specific information into a profile
            as environment variables
- `rich-logging`: improve logging by additional log message formating and bring more colors which 
            improve logs readability
