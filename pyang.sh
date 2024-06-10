#!/bin/bash

REPO_ROOT=$(pwd)/$(dirname "$0")
pushd "$REPO_ROOT" || exit
. ./env.sh
popd || exit
"$REPO_ROOT"/bin/pyang "$@"
