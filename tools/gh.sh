#!/bin/sh
set -eu
cd "$(CDPATH= cd "$(dirname "$0")/.." && pwd)"
usage() { printf '%s\n' 'Usage: sh tools/gh.sh runs|view N|view-log N|--allow-ci-write rerun N|--allow-ci-write dispatch [chrome|firefox]' >&2; exit 64; }
allow_write=false
if [ "${1-}" = --allow-ci-write ]; then allow_write=true; shift; fi
case "${1-}" in
    runs) [ "$#" -eq 1 ] || usage ;;
    view|view-log|rerun)
        [ "$#" -eq 2 ] || usage
        case "$2" in ''|*[!0-9]*) usage ;; esac ;;
    dispatch)
        [ "$#" -le 2 ] || usage
        case "${2-chrome}" in chrome|firefox) ;; *) usage ;; esac ;;
    *) usage ;;
esac
case "$1" in
    rerun|dispatch)
        [ "$allow_write" = true ] || { printf '%s\n' 'BLOCKED: CI write needs --allow-ci-write after authorization.' >&2; exit 77; } ;;
esac
[ -n "${GITHUB_REPOSITORY:-}" ] || { printf '%s\n' 'BLOCKED: set GITHUB_REPOSITORY=owner/repo.' >&2; exit 69; }
command -v gh >/dev/null 2>&1 || { printf '%s\n' 'BLOCKED: gh is not installed.' >&2; exit 69; }
# Uses an existing gh login or GH_TOKEN; never prints credentials.
case "$1" in
    runs) exec gh run list -R "$GITHUB_REPOSITORY" --workflow tests.yml --limit 10 ;;
    view) exec gh run view "$2" -R "$GITHUB_REPOSITORY" ;;
    view-log) exec gh run view "$2" -R "$GITHUB_REPOSITORY" --log ;;
    rerun) exec gh run rerun "$2" -R "$GITHUB_REPOSITORY" ;;
    dispatch) exec gh workflow run tests.yml -R "$GITHUB_REPOSITORY" -f "browser=${2-chrome}" ;;
esac
