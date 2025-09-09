# Docker Container Issues and Fixes Summary

This document summarizes all the Docker container issues encountered during the development of this FastAPI backend template and their resolutions.

## Overview

During the development and testing of the Docker configuration for this FastAPI backend template, we encountered several issues that prevented the containers from starting correctly. This document outlines each issue, its root cause, and the solution implemented.

## Issues and Resolutions

### 1. "exec /start.sh: no such file or directory"

**Problem**: The Docker container failed to start with the error message "exec /start.sh: no such file or directory".

**Root Cause**: The [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script was not being properly copied to the container or was not executable.

**Solution**: 
- Ensured the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script was copied to the correct location (`/start.sh`) in the Dockerfile
- Made the script executable with `RUN chmod +x /start.sh`
- Set the entrypoint correctly in the Dockerfile: `ENTRYPOINT ["/start.sh"]`

### 2. "ImportError: Can't find Python file env.py"

**Problem**: Alembic migrations failed with the error "ImportError: Can't find Python file env.py".

**Root Cause**: The Alembic command was being executed from the wrong directory. The [env.py](file://c:\strategy_test\python_backend_structure\app\migrations\env.py) file was located in the `migrations` directory, but the command was being run from the root directory.

**Solution**:
- Modified the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script to change to the `/app` directory where the migrations folder is located
- Run Alembic from within the migrations directory:
  ```bash
  cd /app
  cd migrations
  alembic -c alembic.ini upgrade head
  ```

### 3. "ls: cannot access 'app/migrations/': No such file or directory"

**Problem**: Debugging command in [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) failed with "ls: cannot access 'app/migrations/': No such file or directory".

**Root Cause**: The path was incorrect. Since we had already changed to the `/app` directory, the correct path was just `migrations/`, not `app/migrations/`.

**Solution**: Corrected the path in the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script from `ls -la app/migrations/` to `ls -la migrations/`.

### 4. "Error loading ASGI app. Could not import module 'main'"

**Problem**: The server failed to start with "Error loading ASGI app. Could not import module 'main'".

**Root Cause**: The server was being started from the wrong directory. The [main.py](file://c:\strategy_test\python_backend_structure\app\main.py) file was in the `/app` directory, but the server was being started from the migrations directory.

**Solution**: Added a directory change back to `/app` before starting the server in the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script:
```bash
# Change back to the app directory before starting the server
cd /app

# Start server
echo "Starting server..."
exec "$@"
```

### 5. "file: command not found"

**Problem**: The [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script contained a `file /start.sh` command that failed with "file: command not found".

**Root Cause**: The `file` command is not available in the minimal Python Docker image.

**Solution**: Removed the problematic command from the [start.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/start.sh) script.

## Final Working Configuration

### Dockerfile Key Elements

```dockerfile
# Copy entrypoint script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Set entrypoint
ENTRYPOINT ["/start.sh"]
```

### start.sh Key Elements

```bash
# Run Alembic migrations
cd /app
cd migrations
alembic -c alembic.ini upgrade head

# Change back to the app directory before starting the server
cd /app

# Start server
exec "$@"
```

## Lessons Learned

1. **File Paths**: Always verify file paths in container environments, as they may differ from the host environment.

2. **Working Directory**: Be mindful of the current working directory when running commands in scripts.

3. **Minimal Images**: Minimal Docker images may not include common utilities. Avoid using commands that may not be available.

4. **Directory Changes**: When changing directories in scripts, ensure you return to the appropriate directory for subsequent commands.

5. **Debugging**: Use `ls -la` and `pwd` commands to debug file and directory issues in container environments.

## Verification

After implementing all fixes, the containers start successfully and the application is accessible at `http://localhost:8088`. The logs show:
- Postgres database ready
- Alembic migrations running successfully
- Server starting with "Uvicorn running on http://0.0.0.0:8088"

This configuration provides a solid foundation for Docker-based deployments of FastAPI applications.