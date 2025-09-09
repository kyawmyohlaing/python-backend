# Docker Container Troubleshooting Guide

This document outlines the issues encountered during the Docker container setup for the FastAPI backend and their resolutions.

## Issue 1: "exec /start.sh: no such file or directory"

### Problem
The Docker container failed to start with the error: `exec /start.sh: no such file or directory`

### Root Cause
The [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script was not being properly copied to the container or was not executable.

### Solution
1. Ensured the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script was copied to the correct location in the Dockerfile:
   ```dockerfile
   COPY start.sh /start.sh
   RUN chmod +x /start.sh
   ```
2. Set the entrypoint correctly in the Dockerfile:
   ```dockerfile
   ENTRYPOINT ["/start.sh"]
   ```

## Issue 2: "ImportError: Can't find Python file env.py"

### Problem
Alembic migrations failed with the error: `ImportError: Can't find Python file env.py`

### Root Cause
The Alembic command was being executed from the wrong directory. The [env.py](file://c:\strategy_test\python_backend_structure\app\migrations\env.py) file was located in the `migrations` directory, but the command was being run from the root directory.

### Solution
Modified the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script to:
1. Change to the `/app` directory where the migrations folder is located
2. Run Alembic from within the migrations directory:
   ```bash
   cd /app
   cd migrations
   alembic -c alembic.ini upgrade head
   ```

## Issue 3: "ls: cannot access 'app/migrations/': No such file or directory"

### Problem
Debugging command in [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) failed with: `ls: cannot access 'app/migrations/': No such file or directory`

### Root Cause
The path was incorrect. Since we had already changed to the `/app` directory, the correct path was just `migrations/`, not `app/migrations/`.

### Solution
Corrected the path in the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script:
```bash
# Incorrect
ls -la app/migrations/

# Correct
ls -la migrations/
```

## Issue 4: "Error loading ASGI app. Could not import module 'main'"

### Problem
The server failed to start with: `Error loading ASGI app. Could not import module 'main'`

### Root Cause
The server was being started from the wrong directory. The [main.py](file://c:\strategy_test\python_backend_structure\app\main.py) file was in the `/app` directory, but the server was being started from the migrations directory.

### Solution
Added a directory change back to `/app` before starting the server:
```bash
# Change back to the app directory before starting the server
cd /app

# Start server
echo "Starting server..."
exec "$@"
```

## Issue 5: "file: command not found"

### Problem
The [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script contained a `file /start.sh` command that failed with: `file: command not found`

### Root Cause
The `file` command is not available in the minimal Python Docker image.

### Solution
Removed the problematic command from the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script:
```bash
# Removed this line
file /start.sh
```

## Best Practices Learned

1. **File Paths**: Always verify file paths in container environments, as they may differ from the host environment.

2. **Working Directory**: Be mindful of the current working directory when running commands in scripts.

3. **Minimal Images**: Minimal Docker images may not include common utilities like `file`. Avoid using commands that may not be available.

4. **Directory Changes**: When changing directories in scripts, ensure you return to the appropriate directory for subsequent commands.

5. **Debugging**: Use `ls -la` and `pwd` commands to debug file and directory issues in container environments.

## Final Working Configuration

### Dockerfile
```dockerfile
# Use slim Python image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app .

# Copy entrypoint script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 8088

# Set entrypoint
ENTRYPOINT ["/start.sh"]

# Command for Gunicorn + Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8088"]
```

### start.sh
```bash
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
```

This troubleshooting guide should help future developers quickly identify and resolve similar Docker container issues.