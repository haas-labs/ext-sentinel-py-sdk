# Version Command

```sh
$ sentinel version --help

usage: sentinel version [--all]

Print Sentinel version and required libs

options:
  -h, --help  show this help message and exit
  --all       also display python/platform/libs info (useful for bug reporting)
```

Shows Sentinel SDK version
```sh
$ sentinel version

{"Sentinel": "v0.3.9.dev4"}
```

and additional required lib details 
```sh
$ sentinel version --all | jq .

{
  "sentinel-sdk": "v0.3.9.dev4",
  "httpx": "0.26.0",
  "python": "3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0]",
  "platform": "Linux-6.5.0-25-generic-x86_64-with-glibc2.35",
  "jinja2": "3.1.3",
  "async_lru": "2.0.4",
  "aiokafka": "0.10.0",
  "pydantic": "2.6.1",
  "web3": "6.15.1",
  "websockets": "12.0"
}
```
