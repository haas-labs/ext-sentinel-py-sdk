# Sentinel Python SDK

Sentinel Python SDK is a library for building and running on-chain data processors and sending events to [Extractor](https://extractor.live).

Detector Examples:
- Contract Attacks
- Liquidity Monitoring
- DEX Activity
- Large Funds transfers
- MEV Artbitrage
- Spam Detection
- Labels collection
- ...

Sentinel supports all blockchain networks supported by [Extractor](https://extractor.live) (e.g. Ethereum,Arbitrum,BSC,...). Please, visit [Extractor](https://extractor.live) for full list of supported networks

## Installation

- [Installation: common steps](docs/Install/Install.md)
- [Python Virtual Environment](Virt-Environment.md) (Recommended)
- [Dev Container Setup](Dev-Container.md) (Optional)

## How to use Sentinel commands

Sentinel Python SDK includes command line interface for launching processes. After the installation steps, described above, you should have `sentinel` command available in your terminal or VS Code shell. 

In VS Code environment, call Terminal (Ctrl-`) or via menu View -> Terminal and type

- [Sentinel Commands](docs/Commands/Main.md)
- [Launch Command](docs/Commands/Launch.md) to run detector/monitor/... from a profile or a bundle
- [Fetch Command](docs/Commands//Fetch.md) to fetch different datasets via RPC and store them locally as files
- [ABI Signatures Command](docs/Commands/ABI-Signatures.md) to git ABI signatures for contract

## Detectors

The role of the detector is to identify various events that have occurred in blockchain's transactions

- [BlockTx Example](examples/block_tx/README.md)
- [Transaction Example](examples/transaction/README.md)
- [Extrctor Attack Detectors](https://github.com/haas-labs/ext-sentinel-detectors-py)

## Tutorials

[BlockTx Detector](examples/block_tx/README.md) provides step-by-step guide and information

## The Bundle

The processes bundle allows to run several processes in one docker container.
