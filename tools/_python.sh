#!/bin/sh
# Shared interpreter selection; source from a tools/*.sh entry point.
set -eu
cd "$(CDPATH= cd "$(dirname "$0")/.." && pwd)"
if [ -n "${PYTHON:-}" ]; then
    harness_python=$PYTHON
elif [ -x .venv/bin/python ]; then
    harness_python="$PWD/.venv/bin/python"
else
    harness_python=python3
fi
command -v "$harness_python" >/dev/null 2>&1 || {
    printf '%s\n' 'BLOCKED: Python not found; set PYTHON to an interpreter executable.' >&2
    exit 69
}
