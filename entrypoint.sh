#!/bin/bash
set -e

# Wait for Postgres
echo "Waiting for Postgres..."
until pg_isready -h db -U postgres; do
  sleep 1
done
echo "Postgres ready!"

# Run migrations
alembic -c app/migrations/alembic.ini upgrade head

# Start server (use Gunicorn for prod or Uvicorn for dev)
exec "$@"