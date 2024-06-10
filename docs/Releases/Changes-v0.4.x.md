# Change Log

## 0.4.9

Feature

- Add database name for blacklist db 

## 0.4.8

Feature

- Local and remote blacklist db (#254)
- Kafka group id in logs (#251)

Documentation

- Add details about required vscode extentions (#253)
- Add recommended vscode configuration (#252)

## v0.4.7

Feature

- Update python packages

## v0.4.6

Feature

- Implement Async Fetcher

## v0.4.5

Refactoring

- Remove check supported networks in tracer (#245)

## v0.4.4

Refactoring

- handle HTTP code 200 for creating/update Label DB records

## v0.4.3

Feature

- add new chain definitions (#240)
- use base58 for IPFS hash (#239)
- handle CGRP token bytecode (#237)
- get contract bytecode and hash, use solc version in format of int list
- extract metadata from contract bytecode (#236)
- add base64 encode/decode utils
- add bytecode metadata parser
- add cbor2 package for parsing bytecode metadata fields
- add fetch code command option (#235)
- integrate metrics db with metrics server (#234)
- add metrics handling where no labels (#233)
- add metric formatter (#232)
- add prometheus text formatter and tests
- activate telemetry for simple tx detector (#230)
- add metric registry in core sentry
- add telemetry settings (#229)
- add metrics sending via queue (#227)
- add sentry metrics serializer (#226)
- add sentry metrics registry (#225)
- add sentry metrics collectors (#224)
- add  metrics sentry and queue (#223)

Documentation

- update contract bytecode and tools
- add contract bytecode details
- add Contract Metadata details
- add settings for telemetry activation and configuration

Tests

- add pytest benchmark

## v0.4.2

Fix

- Block timestamp format in:
  - sentinel fetch command for transactions
  - case of use `use_current_time` for `sentinel.channels.fs.InboundTransactionsChannel`

## v0.4.1

Feature

- Multiple auth service endpoints support

## v0.4.0

Feature

- Sentry only approach

