#!/bin/bash
set -euo pipefail

function docker-run {
    local platform="$1"
    local arch="$2"
    local workdir="/tmp/blurhash-python"

    docker run --rm -e "PLAT=$platform" -v "$(pwd)":"$workdir" -w $workdir \
        -u "$(id -u):$(id -g)" --arch "$arch" "quay.io/pypa/$platform" "${@:3}"
}

python -m build -s
docker-run manylinux_2_28_x86_64 amd64 ./build.sh
docker-run manylinux_2_28_aarch64 arm64 ./build.sh
