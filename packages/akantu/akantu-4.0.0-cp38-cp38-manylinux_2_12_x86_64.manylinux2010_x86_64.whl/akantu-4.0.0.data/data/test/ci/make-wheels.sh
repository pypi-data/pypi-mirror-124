#!/usr/bin/env bash
set -eo pipefail

set +x

export PLAT=manylinux2010_x86_64

source /etc/profile

function repair_wheel {
    wheel="$1"
    if ! auditwheel show "$wheel"; then
        echo "Skipping non-platform wheel $wheel"
    else
        auditwheel repair "$wheel" --plat "$PLAT"
    fi
}

# Compile wheels
for PYBIN in /opt/python/cp3*/bin; do
#    ccache --zero-stats
    echo "${PYBIN}/pip" wheel . --no-deps -w dist/
    "${PYBIN}/pip" wheel . --no-deps -w dist/
#    ccache --show-stats
done

# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    echo repair_wheel "$whl"
    repair_wheel "$whl"
done
