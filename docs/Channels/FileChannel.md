# File Channel

## Inbound File Channel

```yaml
  - name: transactions
    type: sentinel.channels.fs.transactions.InboundTransactionsChannel
    parameters:
      path: samples/block_tx/data/transactions.json
```

## Outbound File Channel

```yaml
  - name: events
    type: sentinel.channels.fs.common.OutboundFileChannel
    parameters:
      record_type: sentinel.models.event.Event
      path: samples/block_tx/events/simple-block-tx.json
      mode: overwrite
```
