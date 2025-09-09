# FastAPI Backend Template Troubleshooting Guide

This guide helps you resolve common issues you might encounter when using the FastAPI backend template.

## 🐳 Docker Issues

### 1. Docker Compose Fails to Start

**Problem:** `make dev` or `docker-compose up` fails to start services.

**Solutions:**
1. Check if Docker is running:
   ```bash
   docker --version
   ```
2. Ensure you have sufficient system resources (RAM, CPU)
3. Check for port conflicts:
   ```bash
   lsof -i :8000
   lsof -i :5432
   ```
4. Restart Docker daemon if needed

### 2. Permission Denied Errors

**Problem:** Permission errors when running Docker commands.

**Solutions:**
1. On Linux, add your user to the docker group:
   ```bash
   sudo usermod -aG docker $USER
   ```
2. Log out and log back in
3. On Windows/macOS, ensure Docker Desktop is running with proper permissions

### 3. Volume Mounting Issues

**Problem:** Changes in code are not reflected in the container.

**Solutions:**
1. Ensure you're running in development mode (`make dev`)
2. Check that volumes are properly configured in `docker-compose.override.yml`
3. Verify file permissions on mounted volumes

## 🗃️ Database Issues

### 1. Database Connection Failed

**Problem:** Application cannot connect to the PostgreSQL database.

**Solutions:**
1. Check if the database container is running:
   ```bash
   docker-compose ps
   ```
2. Verify database credentials in `.env` file
3. Check the `DATABASE_URL` format:
   ```
   postgresql://user:password@host:port/database
   ```
4. Ensure the database service name matches in Docker Compose:
   ```yaml
   # In docker-compose.yml
   services:
     db:  # This is the service name
       # ...
   
   # In .env or environment variables
   DATABASE_URL=postgresql://user:password@db:5432/database
   ```

### 2. Migration Errors

**Problem:** Alembic migrations fail to apply.

**Solutions:**
1. Check migration file syntax:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini check
   ```
2. Verify database connectivity:
   ```bash
   docker-compose exec web pg_isready -h db -U postgres
   ```
3. Check if migrations have already been applied:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini current
   ```
4. Reset migrations if needed:
   ```bash
   docker-compose down -v
   make dev
   ```

### 3. Seeding Data Issues

**Problem:** Example user is not created or accessible.

**Solutions:**
1. Check if the seed migration ran:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini show 0002
   ```
2. Verify data in the database:
   ```bash
   docker-compose exec db psql -U postgres -d mydb -c "SELECT * FROM users;"
   ```
3. Run migrations manually:
   ```bash
   docker-compose exec web alembic -c app/migrations/alembic.ini upgrade head
   ```

## 🔐 Authentication Issues

### 1. Login Fails with "Invalid email or password"

**Problem:** Unable to login with correct credentials.

**Solutions:**
1. Verify the user exists in the database
2. Check if the password was properly hashed during registration
3. Ensure the password hashing algorithm matches between registration and login
4. Check for whitespace or encoding issues in credentials

### 2. JWT Token Expired

**Problem:** API requests return 401 Unauthorized.

**Solutions:**
1. Obtain a new token by logging in again
2. Check the `ACCESS_TOKEN_EXPIRE_MINUTES` setting in `.env`
3. Verify the system time is correct on both client and server

### 3. "Invalid token" Error

**Problem:** Token validation fails even with a recently obtained token.

**Solutions:**
1. Verify the `SECRET_KEY` is consistent between token creation and validation
2. Check if the token was properly extracted from the login response
3. Ensure the Authorization header format is correct:
   ```
   Authorization: Bearer <token>
   ```

## 🌐 Network and API Issues

### 1. API Endpoints Return 404

**Problem:** API endpoints are not found.

**Solutions:**
1. Check if the FastAPI application is running:
   ```bash
   docker-compose logs web
   ```
2. Verify the route prefixes in the route files
3. Ensure routes are properly included in `app/main.py`

### 2. CORS Issues

**Problem:** Frontend requests are blocked by CORS policy.

**Solutions:**
1. Add CORS middleware to `app/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # Configure appropriately for production
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
2. Configure allowed origins in `.env` file

### 3. Slow API Responses

**Problem:** API endpoints take too long to respond.

**Solutions:**
1. Check database query performance
2. Add database indexes for frequently queried columns
3. Implement caching for expensive operations
4. Optimize SQL queries
5. Check for N+1 query problems

## 🧪 Testing Issues

### 1. Tests Fail to Run

**Problem:** `make test` or `pytest` fails to execute.

**Solutions:**
1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```
2. Check if pytest is installed:
   ```bash
   python -m pytest --version
   ```
3. Verify Python path and virtual environment

### 2. Database Tests Fail

**Problem:** Tests that interact with the database fail.

**Solutions:**
1. Ensure test database is accessible
2. Check test database URL configuration
3. Verify database migrations are applied in test environment
4. Check for transaction rollback issues in tests

### 3. Test Coverage Issues

**Problem:** Coverage reports show missing coverage.

**Solutions:**
1. Ensure all code paths are tested
2. Add tests for error conditions
3. Check if tests are actually executing the code
4. Verify coverage configuration

## 🐍 Python and Dependency Issues

### 1. Module Import Errors

**Problem:** Python cannot find modules.

**Solutions:**
1. Check Python path:
   ```bash
   python -c "import sys; print(sys.path)"
   ```
2. Verify package installation:
   ```bash
   pip list | grep package_name
   ```
3. Ensure `__init__.py` files exist in package directories

### 2. Version Conflicts

**Problem:** Dependency version conflicts cause errors.

**Solutions:**
1. Check `requirements.txt` for conflicting versions
2. Use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Update dependencies to compatible versions

### 3. Environment Variables Not Loaded

**Problem:** Environment variables are not accessible in the application.

**Solutions:**
1. Verify `.env` file exists and is properly formatted
2. Check if `python-dotenv` is installed:
   ```bash
   pip install python-dotenv
   ```
3. Ensure `load_dotenv()` is called in `app/config.py`

## 📦 Deployment Issues

### 1. Production Build Fails

**Problem:** `make prod` or production deployment fails.

**Solutions:**
1. Check Dockerfile syntax
2. Verify all dependencies are available
3. Ensure build context is correct
4. Check resource limits (memory, CPU)

### 2. Gunicorn Worker Errors

**Problem:** Gunicorn workers fail to start or restart frequently.

**Solutions:**
1. Check worker count is appropriate for system resources
2. Verify application code doesn't have startup errors
3. Check Gunicorn logs:
   ```bash
   docker-compose logs web
   ```
4. Adjust worker class if needed

### 3. SSL/HTTPS Configuration

**Problem:** HTTPS requests fail or certificates are invalid.

**Solutions:**
1. Ensure SSL certificates are properly configured
2. Check certificate paths and permissions
3. Verify reverse proxy configuration (Nginx, Apache)
4. Test with self-signed certificates for development

## 🛠️ Development Environment Issues

### 1. Hot Reload Not Working

**Problem:** Code changes are not reflected without restarting the server.

**Solutions:**
1. Ensure you're running in development mode (`make dev`)
2. Check that volume mounting is configured correctly
3. Verify file watching is enabled in the development server
4. Check for file permission issues

### 2. IDE Integration Issues

**Problem:** IDE doesn't recognize project structure or dependencies.

**Solutions:**
1. Configure Python interpreter to use the project's virtual environment
2. Install dependencies in the development environment
3. Configure IDE to recognize the project structure
4. Add type stubs for better IDE support

## 🐛 Code and Type Issues

### 1. Type Error with Column[str] in UserService

**Problem:** Static type checkers report an error when accessing user progress:
```
Argument of type "Column[str]" cannot be assigned to parameter "s" of type "str | bytes | bytearray" in function "loads"
```

**Cause:** Some type checkers or IDEs might interpret `db_user.progress` as the Column definition rather than the actual value from the database record when accessing attributes directly.

**Solutions:**
1. Use `getattr()` to explicitly access the attribute value:
   ```python
   # Instead of:
   progress = json.loads(db_user.progress) if db_user.progress else {}
   
   # Use:
   progress_str = getattr(db_user, 'progress', None)
   progress = json.loads(progress_str) if progress_str else {}
   ```

2. Add type ignore comment for assignment operations:
   ```python
   db_user.progress = json.dumps(progress)  # type: ignore
   ```

3. This approach ensures we're working with the actual database value rather than the Column object, making it clear to both the runtime and static analysis tools.

## 📊 Monitoring and Logging Issues

### 1. Logs Not Appearing

**Problem:** Application logs are not visible.

**Solutions:**
1. Check logging configuration in the application
2. Verify log levels are set appropriately
3. Check Docker logging configuration
4. Ensure stdout/stderr are not redirected

### 2. Performance Monitoring

**Problem:** Unable to monitor application performance.

**Solutions:**
1. Add application performance monitoring (APM) tools
2. Implement custom metrics collection
3. Use logging to track performance indicators
4. Set up external monitoring services

## 🆘 Getting Additional Help

If you're still experiencing issues:

1. Check the [FastAPI documentation](https://fastapi.tiangolo.com/)
2. Review the [SQLAlchemy documentation](https://docs.sqlalchemy.org/)
3. Consult the [Docker documentation](https://docs.docker.com/)
4. Search for similar issues on Stack Overflow
5. Open an issue on the GitHub repository with:
   - Detailed error messages
   - Steps to reproduce
   - Environment information (OS, Docker version, etc.)
   - Relevant configuration files