# Python Virtual Environment for Sentinel SDK Developers

Please clone the repository from Github
```sh
git clone https://github.com/haas-labs/ext-sentinel-py-sdk
cd ext-sentinel-py-sdk
```

## Configuration

To configure environment for local development, please run next commands

```sh
./scripts/venv   # to check if virt env created, if no them configure
```

## Activation

```sh
source .venv/bin/activate       # for bash/zsh shell
source .venv/bin/activate.fish  # for fish shell
```
> Please check that you have `(.venv)` in command prompt

## Installation required packages and tools

To install all required packages and tools for local development. Required only first time and after SDK update
```sh
./scripts/install
```

## How to deactivate virtual environment

```sh
deactivate
```
`(.venv)` will be removed from a command prompt


## References

- [venv — Creation of virtual environments](https://docs.python.org/3.11/library/venv.html)

