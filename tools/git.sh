#!/bin/sh
set -eu
cd "$(CDPATH= cd "$(dirname "$0")/.." && pwd)"
[ "$#" -eq 1 ] || { printf '%s\n' 'Usage: sh tools/git.sh status|diff|check' >&2; exit 64; }
export GIT_OPTIONAL_LOCKS=0
case "$1" in
    status) git --no-pager -c core.fsmonitor=false status --short -- . ;;
    diff)
        git --no-pager -c core.fsmonitor=false diff --no-ext-diff --no-textconv -- .
        git --no-pager -c core.fsmonitor=false diff --cached --no-ext-diff --no-textconv -- . ;;
    check)
        git --no-pager -c core.fsmonitor=false diff --check --no-ext-diff --no-textconv -- .
        git --no-pager -c core.fsmonitor=false diff --cached --check --no-ext-diff --no-textconv -- . ;;
    *) printf '%s\n' 'Usage: sh tools/git.sh status|diff|check' >&2; exit 64 ;;
esac
