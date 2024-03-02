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

The next steps, the installation of Sentinel SDK. Strongly recommended to install Sentinel Python SDK in a dedicated virtual environment on all platforms, to avoid conflicting with your system packages.

Virtual environments allow you do not conflict with already-installed Python system packages, which could break some of your system tools and scripts, and still install packages normally with `pip` (without `sudo`).

- [Python Virtual Environment](/docs/Install/Virtualenv.md) (Recommended)
- [Dev Container Setup](/docs/Install/Dev-Container.md) (Optional)

To get more options how to install different SDK version, please follow the guide [How to install specific SDK version](/docs/Install/Howto-Install-Specific-SDK-Version.md)
