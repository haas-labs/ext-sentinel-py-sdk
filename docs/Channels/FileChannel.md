# File Channel

The file channel, similar to [Kafka Channels](/docs/Channels/KafkaChannels.md), used for consuming and publishing data with difference that we are working with local data. It can be useful during detector or monitor development, research, testing. When you need to have consistent collection of transactions and check results.

To prepare the list of transaction and store them in file, please follow the instructions for [How to work with transaction data locally](/docs/Tutorials/How-to-work-with-transaction-data-locally.md) 

## Inbound File Channel

```yaml
  - id: local/fs/transactions
    type: sentinel.channels.fs.transactions.InboundTransactionsChannel
    parameters:
      path: ./data/transactions.json
```

## Outbound File Channel

```yaml
  - id: local/fs/events
    type: sentinel.channels.fs.common.OutboundFileChannel
    parameters:
      record_type: sentinel.models.event.Event
      path: ./data/events.json
      mode: overwrite
```

or more simple configuration for events

```yaml
- id: local/fs/events
  type: sentinel.channels.fs.events.OutboundEventsChannel
  parameters:
    path: monitored_address/data/events/events.json
    mode: overwrite
```
