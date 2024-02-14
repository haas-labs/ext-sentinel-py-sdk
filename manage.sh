#!/bin/bash

set -euo pipefail

SENTINEL_VERSION="0.2.0"

help() {

    echo
    echo "Usage: ./manage.sh <command>"
    echo ""
    echo "Commands:"
    echo
    echo " - cleanup"
    echo " - list-images"
    echo " - remove-images"
    echo 
    echo " - build-base-image"
    echo " - build-dev-image"
    echo " - build-bundle-image"
    echo " - build-all"
    echo 
}

list-images() {

    echo "[INFO] Listing docker images" \
    && docker images "ext/sentinel*/*"
}

cleanup() {

    echo "[INFO] Removing exited containers"
    EXITED_CONTAINERS=`docker ps -a -f status=exited -q`
	if [ ! -z "${EXITED_CONTAINERS}" ]
	then
        docker container rm ${EXITED_CONTAINERS}
	else
		echo "[WARNING] No containers for cleanup"
	fi

    echo "[INFO] Removing dangling images"
	DANGLING_IMAGES=`docker images -f 'dangling=true' -q`
	if [ ! -z "${DANGLING_IMAGES}" ]
	then
		docker image rm ${DANGLING_IMAGES}
	else
		echo "[WARNING] No images for cleanup"
	fi
}

remove-images() {

    echo "[INFO] Removing ext/sentinel images from local" \
        && docker images "ext/sentinel*/*" --quiet | xargs docker image rm \
        && docker images "ext/sentinel*" --quiet | xargs docker image rm   
}

build-base-image() {

    echo "[INFO] Building base image" \
    && docker build \
        -t ext/sentinel/base:v${SENTINEL_VERSION} \
        -f docker/Dockerfile.base . 
}

build-dev-image() {

    echo "[INFO] Building dev image" \
    && docker build \
        -t ext/sentinel/dev:v${SENTINEL_VERSION} \
        -f docker/Dockerfile.dev . 
}

build-bundle-image() {

    echo "[INFO] Building bundle image" \
    && docker build \
        -t ext/sentinel/bundle:v${SENTINEL_VERSION} \
        -f docker/Dockerfile.bundle . 
}

build-all-images() {

    build-base-image \
    && build-dev-image \
    && build-bundle-image
}

$@
