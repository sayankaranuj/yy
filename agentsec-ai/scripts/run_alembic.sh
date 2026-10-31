#!/usr/bin/env sh
SERVICES="postgres redis backend"
WAIT_SECONDS=120

echo "Bringing up Docker Compose services: $SERVICES"
docker compose up -d $SERVICES

echo "Waiting for services to become healthy (up to $WAIT_SECONDS seconds)..."
elapsed=0
while [ $elapsed -lt $WAIT_SECONDS ]; do
  ready=1
  for s in $(docker compose ps --format "{{.Service}} {{.State}}" | awk '{print $2}'); do
    if [ "$s" != "running" ]; then ready=0; break; fi
  done
  if [ $ready -eq 1 ]; then break; fi
  sleep 3
  elapsed=$((elapsed + 3))
done

echo "Applying Alembic migrations inside backend container..."
docker compose exec -T backend /bin/sh -c "alembic upgrade head"

echo "Alembic finished. To inspect DB run: docker compose exec -T postgres psql -U $POSTGRES_USER -d $POSTGRES_DB -c '\d'"
