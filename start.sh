#!/bin/bash
set -e

# Wait for Postgres using Python instead of pg_isready or netcat
echo "Waiting for Postgres..."
until python -c "import socket; socket.create_connection(('db', 5432), timeout=5)" 2>/dev/null; do
  sleep 1
done
echo "Postgres ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic -c migrations/alembic.ini upgrade head

# Change back to the app directory before starting the server
cd /app

# Start server
exec "$@"