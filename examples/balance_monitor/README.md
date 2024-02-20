# Account Balance Monitor

Monitors Account/Contract balance (native token)

List of addresses:

- File with addresses (`data/address.list`)

## Running with Extractor Websocket Stream Source

This will stream data from Extractor Websocket proxy and generate Events to `events` directory

```sh
sentinel launch --profile ./profile-ws-extractor.yaml
```

