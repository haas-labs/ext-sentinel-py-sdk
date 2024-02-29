# Packaging in Docker Image

Building Sentinel processes into Docker images allows to deploy these processes in Extractor infrastructure.

## Sentinel Base Docker image

The Sentinel Base Docker image required to minimize building time and compute resources for final docker image with Sentinel processes.

Please be sure than you have Sentinel Base Docker image with required SDK version: `ext/sentinel/base`. To list available docker images with Sentinel SDK
```sh
./scripts/docker list-images

[INFO] Listing docker images
REPOSITORY          TAG       IMAGE ID       CREATED         SIZE
ext/sentinel/base   v0.3.0    1c302b5e7fc8   8 seconds ago   145MB
```
To check Sentinel SDK version:
```sh
docker run -ti --rm --name sentinel-console ext/sentinel/base:v0.3.0 sentinel --version

```

If there is no base image, you can create it with `build-base-image` command. This command will compile current Sentinel SDK from source and build base Docker image
```sh
./scripts/docker build-base-image

[INFO] Building base image
...
[+] Building 0.2s (8/8) 
[INFO] Installed Sentinel SDK: 0.3.6.post7+git.15e70071.dirty
[INFO] Completed successfully
```
The last 2 lines confirm that building based Sentinel SDK docker image completed successfully 

## Building Sentinel Process Docker image

> Building Sentinel Process docker image will be based on Balance Monitor, which is part of Sentilel SDK examples:

To build a docker image, run the next command from `examples/balance_monitor` directory:
```sh
cd examples/balance_monitor/
docker build -t ext/sentinel/balance-monitor:v0.1.0 .
```

as result you should see new/updated docker image 
```sh
scripts/docker list-images

[INFO] Listing docker images
REPOSITORY                     TAG       IMAGE ID       CREATED          SIZE
ext/sentinel/balance-monitor   v0.1.0    02ca2bb063cb   49 seconds ago   145MB
ext/sentinel/base              v0.3.0    1c302b5e7fc8   17 minutes ago   145MB
``` 

To run docker container with balance monitor locally (VPN access to Hacken infrastructure is required)
```sh
docker run -ti --rm --name sentinel-balance-monitor \
      -v (pwd)/profile.yaml:/opt/sentinel/profile.yaml \
      -v (pwd)/../../.envs/local.yml:/opt/sentinel/envs.yaml \
      ext/sentinel/balance-monitor:v0.1.0 \
      launch \
      --profile profile.yaml \
      --env-vars envs.yaml

024-02-29T13:31:07.392 (MainProcess::sentinel.commands.launch:45) [INFO] Sentinel SDK version: 0.3.6.post7+git.15e70071.dirty

2024-02-29T13:31:07.399 (MainProcess::sentinel.dispatcher:114) [INFO] Initializing channel: transactions, type: sentinel.channels.kafka.transactions.InboundTransactionsChannel
2024-02-29T13:31:07.482 (MainProcess::sentinel.channels.kafka.common:19) [INFO] transactions -> Connecting to Kafka: {'bootstrap_servers': 'b-1.haasdevkafka...amazonaws.com,b-2.haasdevkafka...amazonaws.com', 'group_id': 'sentinel-public.transactions', 'auto_offset_reset': 'latest', 'topics': ['ethereum.mainnet.tx']}
2024-02-29T13:31:07.482 (MainProcess::sentinel.dispatcher:114) [INFO] Initializing channel: events, type: sentinel.channels.kafka.events.OutboundEventsChannel
2024-02-29T13:31:07.486 (MainProcess::sentinel.channels.kafka.common:19) [INFO] events -> Connecting to Kafka: {'bootstrap_servers': 'b-1.haasdevkafka...amazonaws.com,b-2.haasdevkafka...amazonaws.com', 'topics': ['extractor.attack-detector.event']}
2024-02-29T13:31:07.486 (MainProcess::sentinel.dispatcher:98) [INFO] Initializing database: address, type: address_store.AddressStore
2024-02-29T13:31:07.487 (MainProcess::address_store:28) [INFO] Imported 3 addresses
2024-02-29T13:31:07.487 (MainProcess::sentinel.dispatcher:140) [INFO] Initializing process: BalanceMonitor, type: processes.BalanceMonitor
2024-02-29T13:31:07.501 (MainProcess::sentinel.dispatcher:178) [INFO] Active processes: ['ethereum@BalanceMonitor']
2024-02-29T13:31:07.503 (ethereum@BalanceMonitor::processes:18) [INFO] User defined init process started
2024-02-29T13:31:07.503 (ethereum@BalanceMonitor::processes:24) [INFO] Using balance threshold: 10.0 (1e-17)
2024-02-29T13:31:07.867 (ethereum@BalanceMonitor::processes:31) [INFO] Initial balance value: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2: 3016332078383479918105029 (3016332.0783834797)
2024-02-29T13:31:07.868 (ethereum@BalanceMonitor::processes:31) [INFO] Initial balance value: 0x61d0c37f406d1b19fbf9b5267887d67400849a7f: 159887027092833305 (0.1598870270928333)
2024-02-29T13:31:07.868 (ethereum@BalanceMonitor::processes:31) [INFO] Initial balance value: 0x6666827e8f2220ddf718193544889f3b482ed072: 19536269218186066807 (19.536269218186067)
2024-02-29T13:31:07.868 (ethereum@BalanceMonitor::sentinel.processes.transaction:87) [INFO] Starting channel, name: transactions
```
