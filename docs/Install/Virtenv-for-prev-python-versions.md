# How to install Sentinel SDK development environment if your python version 3.9-

> The intruction covers a case when your system is Ubuntu 20.04LTS, as example 

Check python version

```sh
$ python3 -V
Python 3.8.10
```

## How to install python 3.10 or 3.11

Install the necessary dependencies to add the repository
```sh
sudo apt install software-properties-common
```

Import Python PPA on Ubuntu
```sh
sudo add-apt-repository ppa:deadsnakes/ppa
```

Refresh APT Sources List for Python PPA on Ubuntu
```sh
sudo apt update
```

## Install desired python version

```sh
sudo apt install python3.10 python3.10-venv 
```
or 
```sh
sudo apt install python3.11 python3.11-venv
```

## Install virtual env 

for python 3.10
```sh
python3.10 -m venv .venv
```
or for python 3.11
```sh
python3.11 -m venv .venv
```
and then proceed with Sentinel SDK Installation instructions started from [Virtual Env Activation](Virtualenv.md#activation)
