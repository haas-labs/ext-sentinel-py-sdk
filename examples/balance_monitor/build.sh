#!/bin/bash

NETWORK=${1:-eth}
VERSION=${VERSION:-0.0.2}

echo "NETWORK: ${NETWORK}"

docker build -f Dockerfile-${NETWORK}.dev -t ext/sentinel/balance-monitor:${VERSION}-${NETWORK} .

