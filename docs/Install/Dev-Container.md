# Development in VS Code Dev Container

Sentinel SDK includes devcontainer (`.devcontainer/devcontainer.json`) configuration which automates a deployment of local development environment. The local development environment has several benefits:
- development and testing perform inside of docker container, no impacts on host machine
- automate installation process for the Sentinel pyhton sdk
- tools for testings included

Requirements:

- VS Code (https://code.visualstudio.com/)
  - The guide how to [developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers)
- Docker (https://www.docker.com/)

Installation steps:

- Build dev docker images
```sh
./scripts/docker build-base-image
./scripts/docker build-dev-image
```

- Clone Sentinel Python SDK
```sh
git clone https://github.com/haas-labs/ext-sentinel-py-sdk
cd ext-sentinel-py-sdk
```
and open repository (as directory) in VS Code. 
```sh
code .
```
VS Code detects dev container configuration and raise the notification:
> Folder contains a Dev Container configuration file. Reopen folder to develop in a container

Choose "Reopen in container"

Note: If no notification, you can press "Ctrl+Shift+P" for calling Command Palette and select `Dev Containers: Reopen in Container`.

After dev container deployment all required tools and libs will be installed. 
