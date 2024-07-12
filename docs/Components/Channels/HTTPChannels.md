# HTTP Channels

The HTTP Channel supports only outbound interface for publishing events for the Extractor. The logic of publishing events similar to `OutboundEventsChannel` (sentinel.channels.kafka.events)

The access to Hacken Cloud is required

## Configuration Examples

```yaml
- id: hacken/cloud/http/event
  type: sentinel.channels.http.outbound.OutboundEventsChannel
  parameters:
    endpoint: {{ env["EXT_HTTP_URL"] }} 
    token: {{ env['EXT_API_TOKEN'] }}
    network: ethereum
```
