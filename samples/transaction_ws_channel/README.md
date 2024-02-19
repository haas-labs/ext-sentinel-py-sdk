# Simple Transaction Detector with Websocket channel

Simple Transaction Detector demostrates how to use and configure inbound transaction websocket channel

```bash
cd samples/transaction_ws_channel/
sentinel launch --profile profile.yaml \
                --env-vars ../../.envs/local.yml \
                --rich-logging
```

Parameters:

- `profile`: the path to a detector profile
- `env-vars`: websocket configuration contains credentials, to avoid commiting sensitive information 
            in a profile, env-vars parameter helps easy import env specific information into a profile
            as environment variables
- `rich-logging`: improve logging by additional log message formating and bring more colors which 
            improve logs readability
