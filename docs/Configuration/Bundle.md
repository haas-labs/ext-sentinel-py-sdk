# Bundles

A bundle allows to run several processes in one docker container. It helps groups different detectors and monitors and run them together. There 

is the example of a bundle. There are 2 detectors, for Ethereum and BSC networks, which consume transaction data from Kafka channel and store results locally, in the file: `transaction/data/events/events.json`

```yaml
project:
  name: Transaction Detector for Ethereum and BSC networks
  description: Transaction Detector provided as example of consuming transactions and collecting metrics
  config:
    monitoring_enabled: true
    monitoring_port: 9091

imports:
- ../profiles/inputs.yaml

sentries:

- name: TxMetricsDetector
  type: transaction.sentry.TxMetricsDetector
  description: >
    The example of simple transactions detector for consiming transaction and collecting metrics around it
  parameters:
    network: ethereum
  inputs:
  - hacken/cloud/kafka/transaction/ethereum
  outputs:
  - transaction/local/fs/event

- name: TxMetricsDetector
  type: transaction.sentry.TxMetricsDetector
  description: >
    The example of simple transactions detector for consiming transaction and collecting metrics around it
  parameters:
    network: bsc
  inputs:
  - hacken/cloud/kafka/transaction/bsc
  outputs:
  - transaction/local/fs/event

outputs:

- id: transaction/local/fs/event
  type: sentinel.channels.fs.events.OutboundEventsChannel
  parameters:
    path: transaction/data/events/events.json
    mode: overwrite

```