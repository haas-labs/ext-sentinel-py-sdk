#!/bin/bash

NETWORK=${1:-eth}

echo "NETWORK: ${NETWORK}"

docker build -f Dockerfile-${NETWORK}.dev -t ext/sentinel/balance-monitor:0.0.1-${NETWORK} .

