# Websocket Channel

The websocket channel is the alternative for [Kafka Channel](KafkaChannels.md) for getting on-chain transaction data in real-time. The difference is that for Kafka channel you need to have the access to Hacken cloud infrastructure. With websocket, the access to on-chain data is available by websocket URL.

The websocket channel is very helpfull during development and testing. Only inbound websocker channel is supported.

## Inbound Websocket Channel

```yaml
- id: hacken/cloud/ws/transaction/ethereum
  type: sentinel.channels.ws.transactions.InboundTransactionChannel
  parameters:
    server_uri: {{ env["ETHEREUM_WS_URL"] }}
```

if you have configured local node

```yaml
- id: local/ws/transaction
  type: sentinel.channels.ws.transactions.InboundTransactionChannel
  parameters:
    server_uri: ws://localhost:9300
```
