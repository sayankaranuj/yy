#!/bin/sh
set -e

# Simple entrypoint: wait for Postgres and Redis, then exec the given command
POSTGRES_HOST=${POSTGRES_HOST:-postgres}
POSTGRES_PORT=${POSTGRES_PORT:-5432}
REDIS_HOST=${REDIS_HOST:-redis}
REDIS_PORT=${REDIS_PORT:-6379}

wait_for_tcp() {
  host=$1
  port=$2
  while ! nc -z "$host" "$port" >/dev/null 2>&1; do
    echo "Waiting for $host:$port..."
    sleep 1
  done
}

echo "Entrypoint: waiting for dependencies..."
wait_for_tcp "$POSTGRES_HOST" "$POSTGRES_PORT"
wait_for_tcp "$REDIS_HOST" "$REDIS_PORT"

echo "Starting: $@"
exec "$@"
