#!/bin/sh
# Simple healthcheck script for the backend service
set -e

HOST=${HEALTHCHECK_HOST:-localhost}
PORT=${HEALTHCHECK_PORT:-8000}
URL="http://$HOST:$PORT/health/ready"

if command -v curl >/dev/null 2>&1; then
  curl -fsS "$URL" >/dev/null
else
  # fallback to wget
  wget -q -O - "$URL" >/dev/null
fi
