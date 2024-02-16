#!/usr/bin/env bash

# to terminate as soon as any command it executes fails, 
# i.e., returns a non-zero exit status. 
set -e

echo "[INFO] Getting current version"

git config --local user.name "github-actions[bot]"
git config --local user.email "github-actions[bot]@users.noreply.github.com"

SDK_VERSION=`hatch version`
hatch version release
NEXT_SDK_VERSION=`hatch version`

git add src/sentinel/version.py
git commit -m "Bump version: ${SDK_VERSION} → ${NEXT_SDK_VERSION}"

echo "[INFO] Tagging and preparing next version"

git tag $NEXT_SDK_VERSION
SDK_VERSION=`hatch version`
hatch version fix,dev

NEXT_SDK_VERSION=`hatch version`

git add src/sentinel/version.py
git commit -m "Bump version: $SDK_VERSION → $NEXT_SDK_VERSION"
git push
git push --tags
