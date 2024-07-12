# Kafka Channels

Kafka Channel is the way how to consume and publish data in production environment. There are available transactions for different chains, events towards the Extractor, user-defined monitoring contract configurations.

## Configuration

To configure Kafka channel there is needed to specify a channen specification

The example of inbound Kafka channel for on-chain transactions

```yaml
- id: hacken/cloud/kafka/transaction/ethereum
  type: sentinel.channels.kafka.transactions.InboundTransactionsChannel
  parameters:
    bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
    topics: 
    - {{ env['KAFKA_INBOUND_ETH_TX_TOPIC'] }}
```

where 
- `id`: channel id, used in sentry configuration as channel reference
- `type`: classpath to a channel
- parameters: the key/value pair for configuring channels

## The examples of Sentry configuration with Kafka channels

```yaml
sentries:

- name: BalanceMonitor
  type: balance_monitor.sentry.BalanceMonitor
  description: >
    Balance Monitor. Monitors Account/Contract balance (native token)
  parameters:
    network: ethereum
    ...
  inputs:
  - hacken/cloud/kafka/transaction/ethereum
  outputs:
  - hacken/cloud/kafka/event
```

where
- `hacken/cloud/kafka/transaction/ethereum`: channel id to inbound channel for consuming real-time on-chain (Ethereum) transaction data from Kafka
- `hacken/cloud/kafka/event`: channel id to outbound channel for publishing events towards the Extractor
