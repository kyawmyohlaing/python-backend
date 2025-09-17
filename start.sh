#!/bin/bash
set -e

# Debug information
echo "Starting start.sh script"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"

# Add current directory to Python path
export PYTHONPATH="/app:$PYTHONPATH"
echo "PYTHONPATH: $PYTHONPATH"

# Wait for Postgres using Python instead of pg_isready or netcat
echo "Waiting for Postgres..."
until python -c "import socket; socket.create_connection(('db', 5432), timeout=5)" 2>/dev/null; do
  sleep 1
done
echo "Postgres ready!"

# Run Alembic migrations
echo "Running Alembic migrations..."
# Change to the migrations directory where alembic.ini is located
cd /app/migrations

# Run alembic migrations from the migrations directory
alembic upgrade head

# Change back to the app directory
cd /app

# Initialize database with sample data
echo "Initializing database with sample data..."
python init_db.py

# Start server
echo "Starting server..."
exec "$@"