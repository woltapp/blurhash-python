#!/bin/bash
set -euo pipefail

function docker-run {
    local workdir="/tmp/blurhash-python"
    docker run --rm -e "PLAT=$1" -v "$(pwd)":"$workdir" -w $workdir \
        -u "$(id -u):$(id -g)" "quay.io/pypa/$1" "${@:2}"
}

docker-run manylinux_2_24_x86_64 ./build.sh
docker-run manylinux_2_24_i686 linux32 ./build.sh
