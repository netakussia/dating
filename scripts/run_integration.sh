#!/usr/bin/env bash
set -euo pipefail

# Run integration tests for recommendation engine.
# Usage: INTEGRATION=1 REDIS_URL=redis://localhost:6379 ./scripts/run_integration.sh

WORKDIR=$(dirname "$0")/..
cd "$WORKDIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed or not in PATH; please run integration tests against an existing Redis instance by setting INTEGRATION=1 and REDIS_URL"
  exit 1
fi

echo "Bringing up docker-compose services (Postgres + Redis)"
# Assumes docker-compose.yml exists and defines postgres & redis services
docker compose up -d --remove-orphans

# Wait for redis to be ready
REDIS_URL=${REDIS_URL:-redis://localhost:6379}
export REDIS_URL
export INTEGRATION=1

echo "Waiting for Redis to accept connections..."
for i in {1..30}; do
  if docker compose exec -T redis redis-cli ping >/dev/null 2>&1; then
    echo "Redis is ready"
    break
  fi
  sleep 1
done

# Determine how to run tests: prefer running pytest on host connecting to published ports.
# If Redis on localhost is reachable, run pytest locally. Otherwise, run pytest inside the 'bot' container.
REDIS_PING_OK=0
if command -v redis-cli >/dev/null 2>&1; then
  if redis-cli -h 127.0.0.1 -p 6379 ping >/dev/null 2>&1; then
    REDIS_PING_OK=1
  fi
fi

echo "Running integration pytest suite... (REDIS_PING_OK=${REDIS_PING_OK})"
if [ "$REDIS_PING_OK" -eq 1 ]; then
  INTEGRATION=1 REDIS_URL=${REDIS_URL:-redis://localhost:6379} ./venv/bin/pytest -q tests/integration
  STATUS=$?
else
  # Try running inside the 'bot' service container where Docker Compose network is available
  if docker compose ps --services | grep -q '^bot$'; then
    echo "Running tests inside docker-compose 'bot' service"
  # Prefer using virtualenv if present inside container
  # When running inside the 'bot' container, force the compose network address for Redis (redis) so tests connect to the redis service.
  docker compose exec -T bot /bin/sh -lc "if [ -x .venv/bin/python ]; then export INTEGRATION=1 REDIS_URL=redis://redis:6379 && .venv/bin/python -m pytest -q tests/integration; else export INTEGRATION=1 REDIS_URL=redis://redis:6379 && pytest -q tests/integration; fi"
  STATUS=$?
  else
    echo "'bot' service not found in compose. Attempting to run tests in any running service."
    # pick the first running service and execute tests there
    SERVICE=$(docker compose ps --services | head -n1)
    if [ -n "$SERVICE" ]; then
      echo "Running tests inside container: $SERVICE"
      docker compose exec -T "$SERVICE" /bin/sh -lc "export INTEGRATION=1 REDIS_URL=${REDIS_URL:-redis:6379} && pytest -q tests/integration"
      STATUS=$?
    else
      echo "No running compose services found to run tests inside."
      STATUS=2
    fi
  fi
fi

echo "Tearing down docker-compose services"
docker compose down

exit $STATUS
