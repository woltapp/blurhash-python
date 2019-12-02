#!/bin/bash
set -euo pipefail

TMPDIST="$(mktemp -d)"
trap "rm -rf '$TMPDIST'" EXIT

for pybin in /opt/python/cp{27,35,36,37,38}-cp*/bin; do
    "${pybin}/pip" wheel -w "$TMPDIST" ".[testing]"
done

for whl in "$TMPDIST"/blurhash_python*.whl; do
    auditwheel repair "$whl" --plat "$PLAT" -w dist
    rm "$whl"
done

for pybin in /opt/python/cp{27,35,36,37,38}-cp*/bin; do
    "${pybin}/pip" install --no-index -f dist -f "$TMPDIST" "blurhash-python[testing]"
    "${pybin}/pytest"
done
