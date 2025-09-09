#!/bin/bash
set -e

# Debug information
echo "Starting start.sh script"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
echo "Listing root directory:"
ls -la /
echo "Checking if start.sh exists:"
ls -la /start.sh

# Wait for Postgres using Python instead of pg_isready or netcat
echo "Waiting for Postgres..."
until python -c "import socket; socket.create_connection(('db', 5432), timeout=5)" 2>/dev/null; do
  sleep 1
done
echo "Postgres ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
cd /app  # Change to the app directory where migrations are located
echo "Current directory after cd: $(pwd)"
echo "Listing app directory:"
ls -la
echo "Listing migrations directory:"
ls -la migrations/
# Run alembic from within the migrations directory
cd migrations
alembic -c alembic.ini upgrade head

# Change back to the app directory before starting the server
cd /app

# Start server
echo "Starting server..."
exec "$@"