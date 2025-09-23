# Testing Guide

This document provides information about the testing setup and how to run tests for the FastAPI backend.

## 🧪 Test Suite Overview

The test suite includes both unit tests and integration tests to ensure the application functions correctly.

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Focus on business logic

### Integration Tests
- Test API endpoints
- Test database interactions
- Test end-to-end workflows

## 🏃 Running Tests

### Prerequisites
1. Make sure the FastAPI server is running on `http://localhost:8088`
2. Ensure the database is accessible

### Running All Tests
```bash
# Using Makefile
make test

# Direct command
pytest

# With Docker
docker-compose exec web pytest
```

### Running Specific Tests
```bash
# Run a specific test file
pytest tests/test_users.py

# Run tests with a specific keyword
pytest -k "user"

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=app --cov-report=html
```

## 🧪 What the Tests Cover

The test scripts verify the following API endpoints:

1. **Health Check** (`GET /health`) - Verifies the server is running
2. **User Registration** (`POST /users/register`) - Tests creating a new user
3. **User Login** (`POST /users/login`) - Tests authenticating a user
4. **Get Current User** (`GET /users/me`) - Tests retrieving authenticated user info
5. **List Users** (`GET /users/`) - Tests retrieving all users

## 📝 Test User Data

The tests use the following test user data:
```json
{
  "name": "API Test User",
  "email": "api_test@example.com",
  "password": "secure_test_password_123"
}
```

## 🛠️ Test Configuration

### Environment Variables
Tests use the following environment variables:
- `TEST_DATABASE_URL` - Database URL for testing
- `TEST_SECRET_KEY` - Secret key for testing

### Test Database
Tests can run against:
- SQLite in-memory database (for unit tests)
- PostgreSQL database (for integration tests)

## 📊 Test Reports

### Generating Coverage Reports
```bash
# Generate coverage report
pytest --cov=app

# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Generate XML coverage report
pytest --cov=app --cov-report=xml
```

### Viewing Coverage Reports
```bash
# Open HTML coverage report
open htmlcov/index.html
```

## 🐛 Debugging Tests

### Verbose Output
```bash
# Run tests with verbose output
pytest -v

# Run tests with extra verbose output
pytest -vv

# Show print statements
pytest -s
```

### Debugging Specific Tests
```bash
# Run a single test
pytest tests/test_users.py::test_user_registration

# Run tests in a class
pytest tests/test_users.py::TestUserAPI
```

### Using pdb Debugger
```bash
# Run tests with debugger
pytest --pdb

# Run tests with debugger on first failure
pytest --pdb-trace
```

## 🧼 Test Cleanup

### Cleaning Test Data
Tests should clean up after themselves, but you can also:

1. **Reset the database:**
   ```bash
   # With Docker
   docker-compose down -v
   docker-compose up --build
   ```

2. **Run migrations:**
   ```bash
   # With Docker
   docker-compose exec web alembic upgrade head
   ```

## 📈 Continuous Integration

### GitHub Actions
The project includes GitHub Actions workflows for:
- Running tests on push and pull requests
- Checking code quality
- Building Docker images

### Test Matrix
Tests run against multiple Python versions:
- Python 3.9
- Python 3.10
- Python 3.11

## 🤖 Automated Testing

### Test Runner Script
The project includes a test runner script that:
- Sets up the test environment
- Runs all tests
- Generates reports
- Cleans up after testing

### Scheduled Tests
Tests can be scheduled to run:
- Daily
- Weekly
- On deployment

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing Guide](https://docs.sqlalchemy.org/en/latest/orm/session_basics.html#session-faq-whentocreate)