# Sentinel Python SDK

Sentinel Python SDK is a library for building and running on-chain data processors and sending events to [Extractor](https://extractor.live).

Detector Examples:
- Contract Attacks
- Liquidity Monitoring
- DEX Activity
- Large Funds transfers
- MEV Arbitrage
- Spam Detection
- Labels collection
- ...

Sentinel supports all blockchain networks supported by [Extractor](https://extractor.live) (e.g. Ethereum,Arbitrum,BSC,...). Please, visit [Extractor](https://extractor.live) for full list of supported networks

## Installation

- [Installation Guides](/docs/Install/Install.md)

## Development

- [VSCode Configuration](/docs/Development/VSCode-Configuration.md)

## How to use Sentinel commands

Sentinel Python SDK includes command line interface for launching processes. After the installation steps described above, you should be able to run `sentinel` command in your terminal or VS Code shell. 

- [Sentinel Commands](docs/Commands/Main.md)
- [Launch Command](docs/Commands/Launch.md) to run detector/monitor/... from a profile or a bundle
- [Fetch Command](docs/Commands//Fetch.md) to fetch different datasets via RPC and store them locally as files
- [ABI Signatures Command](docs/Commands/ABI-Signatures.md) to git ABI signatures for contract

## Sentinel Components

- [Sentry](/docs/Sentry/Overview.md)
- [Channel](/docs/Channels/Overview.md)
- [Database](/docs/Databases/Overview.md)

## Detectors

The role of the detector is to identify various events that have occurred in blockchain's transactions

- [BlockTx Example](examples/block_tx/README.md)
- [Transaction Example](examples/transaction/README.md)
- [Balance Monitor](examples/balance_monitor/README.md)
- [Extrctor Attack Detectors](https://github.com/haas-labs/ext-sentinel-detectors-py)

## Metrics

- [Metrics](/docs/Metrics/Index.md)

## Tutorials

- [Profile](/docs/Tutorials/Profile.md)
- [Template](/docs/Tutorials/Template.md)
- [Bundle](/docs/Tutorials/Bundle.md)
- [How to work with transaction data locally](/docs/Tutorials/How-to-work-with-transaction-data-locally.md)

## Examples

- [BlockTx Detector](examples/block_tx/README.md) provides step-by-step guide and information

## Deployment

- [Packaging Sentinel processes in Docker image](docs/Deployment/Packaging-in-Docker-Image.md)

## The Bundle

The processes bundle allows to run several processes in one docker container.
