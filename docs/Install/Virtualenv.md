# Python Virtual Environment for Sentinel SDK Developers

## Install Pre-requisites

```sh
sudo apt-get install python3.10-venv
```

Please clone the repository from Github
```sh
git clone --depth 1 git@github.com:haas-labs/ext-sentinel-py-sdk.git
cd ext-sentinel-py-sdk
```

## Creating virtual environment (if not exist)

Please be sure that you have created virtual environment in `.venv` directory. If not, you can created with

```sh
python3 -m venv .venv
```
Please be aware that if your system python version is lower than 3.0, you can use [the instruction](Virtenv-for-prev-python-versions.md)


## Activation

```sh
source .venv/bin/activate       # for bash/zsh shell
source .venv/bin/activate.fish  # for fish shell
```
> Please check that you have `(.venv)` in command prompt

## Installation required packages and tools

To install all required packages and tools for local development. Required only first time and after SDK update
```sh
./scripts/install all
```

After installation you should be able to run `sentinel` command in your terminal

```sh
sentinel --help
```

## How to deactivate virtual environment

```sh
deactivate
```
`(.venv)` will be removed from a command prompt

## References

- [venv — Creation of virtual environments](https://docs.python.org/3.11/library/venv.html)
