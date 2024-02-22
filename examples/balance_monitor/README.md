# Account Balance Monitor

Monitors Account/Contract balance (native token)

List of addresses:

- File with addresses (`data/address.list`)

## Running with Extractor Websocket Stream Source

This will stream data from Extractor Websocket proxy and generate Events to `events` directory

```sh
sentinel launch --profile ./profile-ws-extractor.yaml --env-vars .local-vars.yaml
```

In case of using sensitive information in a profile, Sentinel SDK supports placeholders which can be passed to a profile via `--env-vars` parameter. The example of `.local-vars.yaml` file

```yaml
ETHEREUM_PROXY_RPC_ENDPOINT: https://...hacken.cloud/api/v1/rpc3/
```
The profile with placeholders use
```yaml
- name: BalanceMonitor
  type: processes.BalanceMonitor
  description: >
    Balance Monitor
  parameters:
    chain_id: 1
    network: ethereum
    rpc_proxy_node: {{ env['ETHEREUM_PROXY_RPC_ENDPOINT'] }}
    balance_threshold: 10.0
```

This approach could helpful in case of passing common parameters between many Sentinel processes.

## How to build and rub the balance monitor from Docker image

Activate virtual environment
```sh
source .venv/bin/activate
```

Create Sentinel SDK package
```sh
./scripts/build
```
as result, you should have file `ext_sentinel_py_sdk-....dirty-py3-none-any.whl` file in `dist/` directory

Please be sure than you have Sentinel Base Docker image: `ext/sentinel/base`
```sh
./scripts/docker list-images

[INFO] Listing docker images
REPOSITORY          TAG       IMAGE ID       CREATED      SIZE
ext/sentinel/dev    v0.3.0    a6fc1ba88552   3 days ago   191MB
ext/sentinel/base   v0.3.0    228c1b20b13b   3 days ago   144MB
```

If there is no base image, you can created by the next command:
```sh
./scripts/docker build-base-image

[+] Building 48.3s (6/6 FINISHED                                                             [internal] load build definition from Dockerfile.base ... 0.1s
transferring dockerfile: 1.24kB ... 0.0s
[internal] load metadata for docker.io/library/alpine:edge ... 0.0s
[internal] load .dockerignore ... 0.1s
transferring context: 2B ... 0.0s
CACHED [1/2] FROM docker.io/library/alpine:edge ... 0.0s
[2/2] RUN echo "[INFO] Adding Alpine testing repo" ... 47.6s
exporting to image ...0.5s
exporting layers ... 0.4s
writing image sha256:0041a03409... efc52eab571222777c0fe8 ...0.0s
naming to docker.io/ext/sentinel/base:v0.3.0
```
For building balance monitor docker image:
1. Copy `ext_sentinel_py_sdk...whl` to `examples/balance_monitor/` directory
```
cp dist/ext_sentinel_py_sdk-....whl examples/balance_monitor/
```

2. Update `examples/balance_monitor/Dockerfile` with actual Sentinel SDK filename `ext_sentinel_py_sdk...whl` you copied on step 1.
3. Run the next command from `examples/balance_monitor` directory:
```sh
cd examples/balance_monitor/
docker build -t ext/sentinel/balance-monitor:v0.1.0 .
```

To check created docker image, run the next command:
```sh
docker run -ti --rm --name sentinel-balance-monitor ext/sentinel/balance-monitor:v0.1.0

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

To run docker container
```sh
docker run -ti --rm --name sentinel-balance-monitor \
      -v (pwd)/profile.yaml:/opt/sentinel/profile.yaml \
      -v (pwd)/../../.envs/local.yml:/opt/sentinel/envs.yaml \
      -v (pwd)/events/EVENTS.json:/opt/sentinel/events/EVENTS.json \
      ext/sentinel/balance-monitor:v0.1.0 \
      launch \
      --profile profile.yaml \
      --env-vars envs.yaml

```