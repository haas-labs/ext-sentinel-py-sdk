# Sentinel Python SDK

Sentinel Python SDK is a library for building and running different processors based on data from different blockchains

The list of supported chains:
- Ethereum
- Arbitrum
- BSC

One example is a detector process. Please follow the reference about [How to develop and deploy sample detector](samples/block_tx/README.md)

## Detectors

The role of the detector is to identify various events that have occurred in blockchain's transactions

- [BlockTx Example](samples/block_tx/README.md)
- Suspicious Address
  - Suspicious Account
  - Suspicious Account By Transfer
  - Suspicious Contract
- Indirect Transaction towards Monitored Contract
- Monitored Contract
  - Ownership Change
  - Transfer
  - Transactions from Blacklisted addresses
  - Transactions from suspicious accounts/contracts

## The Bundle

The processes bundle allows to run several processes in one docker container

## How to install Sentinel Python SDK locally 

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

## How to launch detector locally

As sample, we can use 'BlockTx' detector (`samples/block_tx/`). There are several required files to run the detector locally:
- `profile.yaml`: contains a detector configuration
- `processes.py`: python code with BlockTx detection logic
- `data/transactions.json`: the file contains sample transactions
- `data/dex.list`: the file contains details about DEX addesses (Decentralized Exchanges)

To run the detector locally:
```sh
sentinel launch --profile samples/block_tx/profile.yaml 

2024-02-15T14:24:20.183 (MainProcess::sentinel.dispatcher:115) [INFO] Initializing channel: transactions, type: sentinel.channels.fs.transactions.InboundTransactionsChannel
2024-02-15T14:24:20.206 (MainProcess::sentinel.dispatcher:115) [INFO] Initializing channel: events, type: sentinel.channels.fs.common.OutboundFileChannel
2024-02-15T14:24:20.209 (MainProcess::sentinel.dispatcher:99) [INFO] Initializing database: dex_addresses, type: sentinel.db.dex.LocalDEXAddresses
2024-02-15T14:24:20.210 (MainProcess::sentinel.db.dex:39) [INFO] Imported 100 DEX addresses
2024-02-15T14:24:20.210 (MainProcess::sentinel.dispatcher:141) [INFO] Initializing process: BlockTxDetector, type: samples.block_tx.processes.BlockTxDetector
2024-02-15T14:24:20.230 (MainProcess::sentinel.dispatcher:184) [INFO] Active processes: ['ethereum@BlockTxDetector']
2024-02-15T14:24:20.232 (ethereum@BlockTxDetector::sentinel.processes.transaction:70) [INFO] Starting channel, name: transactions
2024-02-15T14:24:20.232 (ethereum@BlockTxDetector::sentinel.processes.transaction:70) [INFO] Starting channel, name: events
2024-02-15T14:24:20.233 (ethereum@BlockTxDetector::sentinel.channels.fs.common:87) [INFO] events -> Starting channel for publishing messages to file channel: events
2024-02-15T14:24:20.235 (ethereum@BlockTxDetector::samples.block_tx.processes:42) [WARNING] Detected block_tx transaction: 0x9756341d
2024-02-15T14:24:20.235 (ethereum@BlockTxDetector::samples.block_tx.processes:42) [WARNING] Detected block_tx transaction: 0x9756341e
^C2024-02-15T14:24:24.725 (MainProcess::sentinel.dispatcher:196) [WARNING] Interrupting by user
2024-02-15T14:24:24.725 (MainProcess::sentinel.dispatcher:207) [INFO] Terminating the process: BlockTxDetector
2024-02-15T14:24:24.725 (MainProcess::sentinel.dispatcher:200) [INFO] Completed
```

to interrupt processing, press `Ctrl+C`
