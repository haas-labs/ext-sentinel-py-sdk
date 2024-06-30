# Installation Guides

## Prerequisites

Sentinel Python SDK requires Python 3.10+ installed. Before start, please be sure that `python` 
```sh
$ python3 --version
Python 3.10.12
```

## Sentinel Python SDK installation

Since the SDK package available via a private repo, SSH keys for getting an access to Github repo must be configured first.
- [Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)

The next steps, the installation of Sentinel SDK.

> IMPORTANT! Strongly recommended to install Sentinel Python SDK in a dedicated virtual environment on all platforms, to avoid conflicting with your system packages.

Virtual environments allow you do not conflict with already-installed Python system packages, which could break some of your system tools and scripts, and still install packages normally with `pip` (without `sudo`).

- [Python Virtual Environment](/docs/Install/Virtualenv.md) (Recommended)
- [Python Virtual Environment whem system python version is 3.9-](/docs/Install/Virtenv-for-prev-python-versions.md)
- [Dev Container Setup](/docs/Install/Dev-Container.md) (Optional)

To get more options how to install different SDK version, please follow the guide [How to install specific SDK version](/docs/Install/Howto-Install-Specific-SDK-Version.md)

## Environemnt Settings

Sentinel uses environment variables for getting access to environemnt specific parameters, like Kafka servers, security tokens, etc. There are several ways how to manage environment:

- The settings in environment variables specified from environment itself. For example, from Kubernetes. This approach is typical for dev and prod environments
- For local development and testing with dev enviroment there are ways:
  - to specify all required environment variables as part of virtual environment configuration
  - specify via `sentinel` command line argument `--env-vars`  the path to YAML file with parameters
  - specify the path to configuration file via `SENTINEL_ENV_PROFILE` env variable

