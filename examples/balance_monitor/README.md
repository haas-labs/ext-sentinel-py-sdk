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
ETHEREUM_PROXY_RPC_ENDPOINT: https://...hacken.cloud/api/v1/rpc3/
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
    rpc_proxy_node: {{ env['ETHEREUM_PROXY_RPC_ENDPOINT'] }}
    balance_threshold: 10.0
```

This approach could helpful in case of passing common parameters between many Sentinel processes.