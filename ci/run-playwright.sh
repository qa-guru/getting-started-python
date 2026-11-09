#!/bin/sh
set -eu

# Keep this version aligned with requirements.txt.
image='mcr.microsoft.com/playwright/python:v1.64.1-noble'
workspace=${WORKSPACE:-$(pwd)}

run_playwright() {
    docker run --rm --init --ipc=host \
        --user "$(id -u):$(id -g)" \
        --env HOME=/tmp \
        --env HEADLESS --env BASE_URL --env AUTH_URL --env BROWSER \
        --workdir "$workspace" "$@"
}

# Containerized Jenkins agents usually share their workspace through a volume.
# Reuse those mounts when the agent is visible to the same Docker daemon.
if [ -n "${HOSTNAME:-}" ] && docker container inspect "$HOSTNAME" >/dev/null 2>&1; then
    run_playwright --volumes-from "$HOSTNAME" "$image" "$@"
else
    # For agents running directly on the Docker host.
    run_playwright --mount "type=bind,source=$workspace,target=$workspace" "$image" "$@"
fi
