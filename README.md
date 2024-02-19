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

### "Classical" way

Before start, please be sure that `pip` installed
```sh
git clone https://github.com/haas-labs/ext-sentinel-py-sdk
cd ext-sentinel-py-sdk
pip install --user .
```
for certain systems you can get the error:
> This environment is externally managed. The system-wide python installation should be maintained using the system package manager only.

In this case, the recommended way to install the Sentinel SDK via python virtual environment

```sh
python3 -m venv /path/to/venv
. /path/to/venv/bin/activate
pip install --user .
```

### VS Code with dev container (recommended)

Sentinel SDK includes devcontainer (`.devcontainer/devcontainer.json`) configuration which automates a deployment of local development environment. The local development environment has several benefits:
- development and testing perform inside of docker container, no impacts on host machine
- automate installation process for the Sentinel pyhton sdk
- tools for testings included

Requirements:

- VS Code (https://code.visualstudio.com/)
  - The guide how to [developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)
- Docker (https://www.docker.com/)

Installation steps:

- Build dev docker images
```sh
./manage.sh build-base-image
./manage.sh build-dev-image
```

- Clone Sentinel Python SDK
```sh
git clone https://github.com/haas-labs/ext-sentinel-py-sdk
cd ext-sentinel-py-sdk
```
and open repository (as directory) in VS Code. 
```sh
code .
```
VS Code detects dev container configuration and raise the notification:
> Folder contains a Dev Container configuration file. Reopen folder to develop in a container

Choose "Reopen in container"

Note: If no notification, you can press "Ctrl+Shift+P" for calling Command Palette and select `Dev Containers: Reopen in Container`.

After dev container deployment all required tools and libs will be installed. 

## How to use Sentinel commands

Sentinel Python SDK includes command line interface for launching processes. After the installation steps, described above, you should have `sentinel` command available in your VS Code shell. 

In VS Code environment, call Terminal (Ctrl-`) or via menu View -> Terminal and type
```sh
sentinel 
usage: sentinel [-h] {launch,fetch,abi-signatures} ...

positional arguments:
  {launch,fetch,abi-signatures}
                        Sentinel Commands
    launch              Launch sentinel process(-es)
    fetch               Fetch data via JSON-RPC
    abi-signatures      ABI Signatures Handler

options:
  -h, --help            show this help message and exit
```

## Detectors

The role of the detector is to identify various events that have occurred in blockchain's transactions

- [BlockTx Example](examples/block_tx/README.md)
- [Transaction Example](examples/transaction/README.md)
- [Extrctor Attack Detectors](https://github.com/haas-labs/ext-sentinel-detectors-py)


## Tutorial

[BlockTx Detector](examples/block_tx/README.md) provides step-by-step guide and information

## The Bundle

The processes bundle allows to run several processes in one docker container.

