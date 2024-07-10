# Kafka Channel Examples

## Inbound

Ethereum transactions Kafka Channel

```yaml
- id: hacken/cloud/kafka/transaction/ethereum
  type: sentinel.channels.kafka.transactions.InboundTransactionsChannel
  parameters:
    bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
    topics: 
    - {{ env['KAFKA_INBOUND_ETH_TX_TOPIC'] }}
```

Detectors Configuration

```yaml
- id: hacken/cloud/kafka/monitoring_conditions
  type: sentinel.channels.kafka.config.InboundConfigChannel
  parameters:
    bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
    topics: 
    - extractor.sync.detector
```

## Outbound

Extractor Events Kafka Channel

```yaml
- id: hacken/cloud/kafka/event
  type: sentinel.channels.kafka.events.OutboundEventsChannel
  parameters:
    bootstrap_servers: {{ env['KAFKA_BOOTSTRAP_SERVERS'] }}
    topics: 
    - {{ env['KAFKA_OUTBOUND_EVENT_TOPIC']}}
```