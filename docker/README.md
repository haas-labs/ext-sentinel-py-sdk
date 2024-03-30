# Sentinel SDK Docker images

The directory contains dockerfiles for building docker images:
- base: required for building Sentinel detectors/monitors/... 
- dev: required for local development and testing. For example, this image is helpful to be used in [VS Code devcontainer](https://code.visualstudio.com/docs/devcontainers/containers). Dev image uses the base image and contains extra python packages for SDK testing.

## Version

The version of base Sentinel SDK docker image stored in `/scripts/common`, variable: SENTINEL_DOCKER_VERSION

## How to build docker images

From Sentinel SDK root directory, to build base docker image, run:
```sh
./scripts/docker build-base-image
```

To build dev image, run:
```sh
./scripts/docker build-dev-image
```