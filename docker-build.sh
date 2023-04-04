#!/bin/bash
set -euo pipefail

function docker-run {
    local workdir="/tmp/blurhash-python"
    docker run --rm -e "PLAT=$1" -v "$(pwd)":"$workdir" -w $workdir \
        -u "$(id -u):$(id -g)" "quay.io/pypa/$1" "${@:2}"
}

python -m build -s
docker-run manylinux_2_28_x86_64 ./build.sh
