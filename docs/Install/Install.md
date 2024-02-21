# Install

Sentinel Python SDK requires Python 3.10+ installed. 

Strongly recommend to install Sentinel Python SDK in a dedicated virtual environment on all platforms, to avoid conflicting with your system packages.

Virtual environments allow you to not conflict with already-installed Python system packages, which could break some of your system tools and scripts, and still install packages normally with `pip` (without `sudo`).

## Prerequisites

Before start, please be sure that `python` 
```sh
$ python3 --version
Python 3.10.12
```

and `pip` installed in your system
```sh
$ pip --version
pip 24.0 (python 3.10)
```

## Sentinel Python SDK installation

- [Python Virtual Environment](Virtualenv.md): Recommended
- [Dev Container Setup](Dev-Container.md): Optional

After environment configuration, please proceed with Sentinel Python SDK installation. Since the SDK package available via a private repo, SSH keys for getting an access to Github repo must be configured. 
- [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

To install SDK in virtualenv:
```sh
pip install git+ssh://git@github.com/haas-labs/ext-sentinel-py-sdk.git@v0.3.5
```
To get more options how to install different SDK version, please follow the guide [How to install specific SDK version](/docs/Install/Howto-Install-Specific-SDK-Version.md)

After installation you should be able to run `sentinel` command in your terminal

```sh
sentinel --help
```
## Installation procedure for Sentinel SDK developers

Please follow the [Virtual environment setup for SDK developers](/docs/Install/Virtualenv-for-SDK-Developers.md)
