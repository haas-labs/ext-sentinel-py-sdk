# Account Balance Monitor

Monitors Account/Contract balance (native token)

List of addresses:

- File with addresses (`data/address.list`)

## Running with Extractor Websocket Stream Source

This will stream data from Extractor Websocket proxy and generate Events to `events` directory

```sh
sentinel launch --profile ./profile-ws-extractor.yaml --env-vars .local-vars.yaml
```

In case of using sensitive information in a profile, Sentinel SDK supports placeholders which can be passed to a profile via `--env-vars` parameter. The example of `.local-vars.yaml` file

```yaml
EXT_RPC_URL: https://...hacken.cloud/api/v1/rpc3/
```
The profile with placeholders use
```yaml
- name: BalanceMonitor
  type: processes.BalanceMonitor
  description: >
    Balance Monitor
  parameters:
    chain_id: 1
    network: ethereum
    rpc: {{ env['EXT_RPC_URL'] }}
    balance_threshold: 10.0
```

This approach could helpful in case of passing common parameters between many Sentinel processes.

----

## Running local environment

1. Install foundry suite (anvil, cast)

2. Run anvil
```
anvil --host 0.0.0.0
```

3. Export anvil default wallets

```
source env.anvil
```

4. Run Websocket proxy

On Linux:
```
docker run --rm -p 9300:9300 syspulse/trunk3 -f http://172.17.0.1:8545 -e tx.extractor -o ws:server://0.0.0.0:9300 --format=json --receipt.request=batch --throttle=1000
```

On Mac:
```
docker run --rm -p 9300:9300 syspulse/trunk3 -f http://host.docker.internal:8545 -e tx.extractor -o ws:server://0.0.0.0:9300 --format=json --receipt.request=batch --throttle=1000
```

5. Start `balance_monitor`

```
sentinel launch --profile ./profile-ws-anvil.yaml
```

6. Make transfer transaction

```
cast send $ADDR1 --private-key=$SK2 --value=10 --gas-price=1gwei --priority-gas-price=1gwei --gas-limit=21000
```

### Build Docker for Dev environment

1. Set vars in `env-dev.yaml`:
```
EXTRACTOR_PUBLIC_API_ENDPOINT: https://api.extractor.dev.hacken.cloud

HACKEN_API_TOKEN: JWT

ETH_WS_URL: ws://ethereum-ingest-proxy.dev.hacken.cloud/API_KEY
ETH_RPC_URL: https://rpc3-ethereum-mainnet.hacken.cloud/api/v1/rpc3/API_KEY

BSC_WS_URL: ws://bsc-ingest-proxy.dev.hacken.cloud/API_KEY
BSC_RPC_URL: https://rpc3-bsc-mainnet.hacken.cloud/api/v1/rpc3/API_KEY

KAFKA_BOOTSTRAP_SERVERS: haas-dev-kafka1.hacken.dev:9092
KAFKA_INBOUND_TX_TOPIC: ethereum.mainnet.tx
KAFKA_OUTBOUND_EVENT_TOPIC: extractor.attack-detector.event
```

2. Link or create `profile-dev.yaml` with required settings.

Inputs and Outputs must point to Kafka:

```
  inputs:
  - name: transactions
    type: sentinel.channels.kafka.transactions.InboundTransactionsChannel
    parameters:
      bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
      group_id: sentinel-public.transactions
      auto_offset_reset: latest
      topics: 
      - {{ env['KAFKA_INBOUND_TX_TOPIC'] }}

  outputs:
  - name: events
    type: sentinel.channels.kafka.events.OutboundEventsChannel
    parameters:
      bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
      topics: 
      - {{ env['KAFKA_OUTBOUND_EVENT_TOPIC']}}

```

3. Built image:

```
docker build -f Dockerfile.dev -t ext/sentinel/balance-monitor:0.0.1 .
```

4. Run image

```
docker run -ti --rm --name sentinel-balance-monitor ext/sentinel/balance-monitor:0.0.1
```