# How to work with transaction data locally

Very often during development there is needed to have transaction data locally. Sometimes you need to include transaction data as part of tests to have an option to make regression tests. Getting data via RPC could be costly, required additional connectivity, dependencies on external resources. To avoid it, Sentinel SDK provides the way how to fetch required data once and then use this dataset in a way you need.

First of all, you need to prepare the list of transaction hashes. It should be simple text file where each transaction hash stored in separate line.

The example of the file with transaction hashes
```
0x0dfc10eb166bfa1e27fa76609b5bcd36c4cb1af9d56b1178b8078fbad8442587
0x12e7ff7b0a494afbf05b1f1dbc7b9fcde8bb86b7f87c2707b9f7b0b9ac67fed0
0x77327829261e1e811058be13b17943ab3c1e024e558a6eecdbb71c2a63d84542
...
```
Store it with the name: `tx.hashes`

One of `sentinel` commands is `fetch` command

```sh
$ sentinel fetch --help

usage: sentinel fetch

Fetch data via JSON-RPC

options:
  -h, --help            show this help message and exit
  --rpc RPC             JSON-RPC End-Point
  --dataset {block,transaction,trace,trace_transaction,debug_trace_transaction}
                        Dataset type for fetching
  --from-file FROM_FILE
                        Fetch data from list
  --to-file TO_FILE     Store results into file

global options:
  -L LEVEL, --log-level LEVEL
                        log level (default: INFO)
  --rich-logging        Activate rich logging
```

To fetch transaction data 
```sh
$ sentinel fetch \
    --rpc <JSONRPC-URL> \
    --dataset transaction \
    --from-file tx.hashes \
    --to-file transactions.json
```

As result, the file `transactions.json` will contain transaction details
```json
{"block_hash": "0xa27caf5539eac7637c8c03dab7463c5ce42ef630fae03df19542906f973f6191", "block_number": "0x1a56fcd", "from_address": "0x134bb354793913f9e5dcfa52f12236e02a6438da", "gas": 390000, "gas_price": 3000000000, "hash": "0x0dfc10eb166bfa1e27fa76609b5bcd36c4cb1af9d56b1178b8078fbad8442587", "input": "0xb438689f0000000000000000000000001e34a77868e19a6647b1f2f47b51ed72dede95dd00000000000000000000000000000000000000000000000000000000000001002ac434bc4d29ab8b53aab11b19bfe07e9b2dd19ae5e6d561e39de81a00ed121419bbdfdb3a46f33198cca8665a6a1716e621389bea480b77ab2780674ea9f6d00000000000000000000000000bd94b3745b8bb14230887eaf12a7e2664415dfb000000000000000000000000134bb354793913f9e5dcfa52f12236e02a6438da000000000000000000000000000000000000000000000000009243e5996720000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010024da2188c66d4b661995689b5c19edb51f816b2654ad9d2f7e17c976ab8506292aa9a70297a79dea1cb0ea4e12144367212692b2692aacb31329e0992a6e89221169ca0e63c0c9807b23c385d2f35310a12e363998ccefc6a30eb442cc5af3cf150864af2a0834380321042a69d8b16c5a004ae40b64ff3a348e5e4ee11095c52c9a28f0211b0ed12b5c43b71158b56286cb754fb1189d2289d6bf28dc029eb106f34df809f96d6cc075eb7cd21a3811af5aef2f481936b59811f17a4ad4079a14d9f6cf59cd27bc6c8650bbdbbcaa5d59d466a65e05739ff1cae15c59c309f82f998d021339e607faffbfeb952133cb8c08fe435271bbb2f84543a4e6af8d71", "nonce": 306, "to_address": "0x0d5550d52428e7e3175bfc9550207e4ad3859b17", "transaction_index": 178, "value": 0, "transaction_type": 0, "logs": [{"address": "0x1e34a77868e19a6647b1f2f47b51ed72dede95dd", "topics": ["0xe9e508bad6d4c3227e881ca19068f099da81b5164dd6d62b2eaf1e8bc6c34931", "0x000000000000000000000000134bb354793913f9e5dcfa52f12236e02a6438da"], "data": "0x0000000000000000000000000bd94b3745b8bb14230887eaf12a7e2664415dfb19bbdfdb3a46f33198cca8665a6a1716e621389bea480b77ab2780674ea9f6d0000000000000000000000000000000000000000000000000009243e599672000", "index": 423}], "contract_address": null, "cumulative_gas_used": 19313635, "effective_gas_price": 3000000000, "gas_used": 346696, "status": 1, "block": {"difficulty": 2, "extra_data": "0xd883010117846765746888676f312e31392e38856c696e7578000000f98d1072af5f47d3971e879f82b529f91b75bc64103ad39d583a3e2349fa10ce4b1ceb9b0c83444abc0f593ff16bdd24f046469d20b747d9dbb0d13dff12aa047c50988900", "gas_limit": 139991454, "gas_used": 23431792, "hash": "0xa27caf5539eac7637c8c03dab7463c5ce42ef630fae03df19542906f973f6191", "logs_bloom": "0x5daff3b73b60305b643e6f56f137199ea234630a37b9a7413c3d5ffa6bf35f57fb574156ff7c186af7ab1678761fb7f6398b53e61642f4fb573d52bad8356f2c1682d303914f1efba37a9d2cdb0b5d3f6e5cc0bb04f4eeaa9044be17ca7d979e0b5753625e1abe24b5d3afdec9fbaabbaed5edf9bd8accdfb8e525daafae6cf71bfab9405ebb1fd7e39ab4a7c1704f3a3df61ec5dfe6a49c6578e55394b4dbacce881c8399ffb2b0aede61fe87ef4ef4e24dc49f77f43183b8713b7d6047cd5bbf067fb6225fc3ce93f781b7089affd67775e76d25afc832fd5bc546c946f065e13acc41f430cda92bed1b67352ba874e1548e6cd1fee16cca335d3d1dbd8450", "miner": "0xbe807dddb074639cd9fa61b47676c064fc50d62c", "nonce": "0x0000000000000000", "number": 27619277, "parent_hash": "0x4935169a2ce934f528e6ba18cf264786b675a1207ec6c30b503e13cfb0d9b4c2", "receipts_root": "0x9e7689f7d39de879b7e17ce335af3955fc78af80694fc51ce7782e7f8d9dd827", "sha3_uncles": "0x1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347", "size": 86552, "state_root": "0x7f29910672d5c8676790ea467584c753ed2b2cdfd752e2104b9bb72d6f04601f", "timestamp": 1682313076, "total_difficulty": 54887149, "transactions_root": "0xf3570a77b62992c2b4dae99381fdbd610f354ce8050854f561043880b8bb1a95", "uncles": [], "transaction_count": 223}, "root": null}
```