# Simple Block/Transactions Detector

The goal of simple block/transaction detector to provide a sample how to develop detectors based on Sentinel SDK.

## Requirements for a detector

The detector should 
- collects transactions from a block
- select transactions towards DEX (Distributed Exchanges)
- detect multiple transaction in a block with difference in a gas price 

There are several required files to run the detector locally:
- `profile-<source>.yaml`: contains a detector configuration
- `processes.py`: python code with BlockTx detection logic
- `data/transactions.json`: the file contains sample transactions (only for testing)
- `data/dex.list`: the file contains details about DEX addesses (Decentralized Exchanges)


## General code structure of detector

```python
from sentinel.processes.block import BlockDetector

from sentinel.models.event import Event
from sentinel.models.transaction import Transaction

logger = logging.getLogger(__name__)

class BlockTxDetector(BlockDetector):
    async def on_block(self, transactions: List[Transactions]) -> None:
        '''
        Handle block transactions
        '''
        # Detection logic
        ...
        # Send an event
```

## Profile

The detector code structure helps concentrate more on business logic of detection itself and make it inftrastruture agnosostic. Where an detector profile responsible for integration an detector with an environment:
- Data source(-s): local file system, ASW S3 storage, Kafka, Websocket
- Notification system(-s)
- Integration with local/remote Databases


The sample of profile structure
```yaml

- name: BlockTxDetector
  type: processes.BlockTxDetector
  description: >
    Simple Block/Tx Detector
  ...

  inputs:

  - name: transactions
    ...

  outputs:

  - name: events
    ...

  databases:

  - name: dex_addresses
    ...
```

## Running with Extractor Websocket Stream Source

This will stream data from Extractor Websocket proxy:

```sh
sentinel launch --profile ./profile-ws-extractor.yaml
```


## Running with collected Transaction Files Source 

For local testing, Sentinel SDK has console tool for fetching transactions content in required format based on provided blocks list. To collect it

```sh
sentinel fetch --rpc http://rpc3-ethereum-mainnet.hacken.cloud/api/v1/rpc3 \
               --dataset block \
               --from-file ./data/blocks.list \
               --to-file ./data/transactions.json
```

The content of `blocks.list`
```
0x1238cfe
0x1238cff
```


Example of transactions file:

```json
{
    "block": {
        "parent_hash": "0x272bfd208...",
        "nonce": "0x0000000000000000",
        "sha3_uncles": "0x1dcc4de8dec75d...",
        "logs_bloom": "0xfbb179f362d9",
        "transactions_root": "0x2175892552c...",
        "state_root": "0x0ffbb487958...",
        "receipts_root": "0x88940c7afc02...",
        "miner": "0x95222290dd72...",
        "difficulty": 0,
        "total_difficulty": 58750003716598360000000,
        "size": 118676,
        "extra_data": "0x6265617665726275696c642e6f7267",
        "gas_limit": 30000000,
        "gas_used": 11634581,
        "timestamp": 1699275839,
        "base_fee_per_gas": 36356209015
    },
    "hash": "0x79c5befa7ed2bc...",
    "nonce": 1447,
    "block_hash": "0x8bcca024728...",
    "block_number": 18513117,
    "block_timestamp": 1699275839,
    "transaction_index": 1,
    "from_address": "0xdcf9aa0f05deddffc1cb699795ca9cd0d9d0ae6f",
    "to_address": "0xdb5889e35e379ef0498aae126fc2cce1fbd23216",
    "value": 0,
    "gas": 372702,
    "gas_price": 66356209015,
    "input": "0x70fef1da000000000000...",
    "max_fee_per_gas": null,
    "max_priority_fee_per_gas": null,
    "cumulative_gas_used": 276110,
    "gas_used": 165296,
    "contract_address": null,
    "root": null,
    "status": 1,
    "effective_gas_price": 66356209015,
    "transaction_type": 0,
    "logs": [
        {
            "index": 3,
            "address": "0x3ad9d01c8a...",
            "data": "0x00000000000...",
            "topics": [
                "0xddf252ad1be2c89...",
                "0x000000000000000...",
                "0x000000000000000..."
            ]
        },
        ...
    ]
}

```

Run a detector agains collected data (from Detector directory):

```sh
sentinel launch --profile ./profile-local.yaml
```

The command output
```
2024-02-01T19:58:21.888 (MainProcess::sentinel.dispatcher:122) [INFO] Initializing channel: transactions, type: sentinel.channels.fs.transactions.TransactionsChannel
2024-02-01T19:58:21.899 (MainProcess::sentinel.dispatcher:122) [INFO] Initializing channel: events, type: sentinel.channels.fs.aio.AioProducerFileChannel
2024-02-01T19:58:21.900 (MainProcess::sentinel.dispatcher:106) [INFO] Initializing database: dex_addresses, type: sentinel.db.dex.LocalDEXAddresses
2024-02-01T19:58:21.900 (MainProcess::sentinel.db.dex:39) [INFO] Imported 100 DEX addresses
2024-02-01T19:58:21.900 (MainProcess::sentinel.dispatcher:148) [INFO] Initializing process: BlockTxDetector, type: samples.block_tx.processes.BlockTxDetector
2024-02-01T19:58:21.915 (MainProcess::sentinel.dispatcher:191) [INFO] Active processes: ['BlockTxDetector']
2024-02-01T19:58:21.917 (BlockTxDetector::sentinel.processes.transaction:64) [INFO] Starting channel, name: transactions
2024-02-01T19:58:21.917 (BlockTxDetector::sentinel.processes.transaction:64) [INFO] Starting channel, name: events
2024-02-01T19:58:21.917 (BlockTxDetector::sentinel.channels.fs.aio:85) [INFO] events -> Starting channel for publishing messages to file channel: events
2024-02-01T19:58:21.919 (BlockTxDetector::samples.block_tx.processes:47) [WARNING] Detected block_tx transaction: 0x9756341d
2024-02-01T19:58:21.919 (BlockTxDetector::samples.block_tx.processes:47) [WARNING] Detected block_tx transaction: 0x9756341e

...
```

## How to deploy to Extractor Dev Environment

In current implementation of Sentinel SDK, to deploy a detector to Extractor env, there is needed to commit changes and create a Pull Request (PR) to main. As result of PR complettion, CI/CD pipeline compiles a new docker image and published it to Extractor environment automatically

