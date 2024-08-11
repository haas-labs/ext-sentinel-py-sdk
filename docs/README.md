# Sentinel Python SDK

## Table of Content

- [Installation Guides](Install/Install.md)
- [Configuration](Configuration/Index.md)
- [Development](Development/Index.md)
- [Deployment](Deployment/Index.md)
- [Release Notes](Releases/Release-Notes.md)
- [Sentinel Commands](Commands/Index.md)
- [Sentinel Components](Components/Index.md)
- [Metrics](Metrics/Index.md)
- [Tutorials](Tutorials/Index.md)
- [Tools](Tools/Index.md)

## Overview

Sentinel Python SDK is designed for building custom on-chain and off-chain data processors and detectors

- Research and prototyping, developing production-ready detectors
- Inputs/outputs/databases
  - Local file system and Websocket Data Feed for Testing
  - Kafka Data Feed for Production
  - Event generation
- Seamlessly integrates with [Extractor](https://extractor.live)

## Detector Examples:

- Contract Attacks
- Liquidity Monitoring
- DEX Activity
- Large Funds transfers
- MEV Arbitrage
- Spam Detection
- Labels collection
- ...

Sentinel supports all blockchain networks supported by [Extractor](https://extractor.live) (e.g. Ethereum, Arbitrum, BSC,...). Please, visit [Extractor](https://extractor.live) for full list of supported networks
Sentinel SDK is not limited to build just on-chain data processor, there are options to develop sentries for processing data on schedule.

## What problems does Detector  SDK solve?

- Simplified Research, Development, Testing and Configuration
- Unified Data Sources and Format
- Data Steaming, Batch and Scheduled processing
- Simulation
- Environment Agnostic
- Single and bundled processing
- Reusable Solutions
- Developers and Researchers Collaboration

## Detector and Monitor Examples

The role of the detector is to identify various events that have occurred in blockchain's transactions. Check the `examples/` directory for getting more info

## References

- [Extractor](https://extractor.live)
