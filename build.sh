#!/bin/bash
set -euo pipefail

TMPDIST="$(mktemp -d)"
USERBASE="$(mktemp -d)"
trap "rm -rf '$TMPDIST' '$USERBASE'" EXIT

for pybin in /opt/python/cp{36,37,38,39,310}-cp*/bin; do
    "${pybin}/pip" wheel --no-cache-dir -w "$TMPDIST" ".[testing]"
done

for whl in "$TMPDIST"/blurhash_python*.whl; do
    auditwheel repair "$whl" --plat "$PLAT" -w dist
    rm "$whl"
done

ORIGPATH="$PATH"

for pybin in /opt/python/cp{36,37,38,39,310}-cp*/bin; do
    userbindir="$USERBASE/${pybin#/opt/python/}"
    export PYTHONUSERBASE="${userbindir%/bin}"
    export PATH="$ORIGPATH:$userbindir"
    "${pybin}/pip" install --no-cache-dir --user --no-index -f dist -f "$TMPDIST" "blurhash-python[testing]"
    "${userbindir}/pytest"
done
