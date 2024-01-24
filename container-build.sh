#!/bin/bash
set -euo pipefail

function podman-run {
    local platform="$1"
    local arch="$2"
    local workdir="/tmp/blurhash-python"

    podman run --rm \
        -e "PLAT=$platform" \
        -v "$(pwd)":"$workdir" \
        -w $workdir \
        --userns keep-id \
        --arch "$arch" \
        "quay.io/pypa/$platform" "${@:3}"
}

python -m build -s
podman-run manylinux_2_28_x86_64 amd64 ./build.sh
podman-run manylinux_2_28_aarch64 arm64 ./build.sh
