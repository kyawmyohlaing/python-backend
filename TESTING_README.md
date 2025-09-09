# API Testing Guide

This guide explains how to use the API testing scripts provided with the FastAPI Backend Template.

## 📋 Available Test Scripts

1. **[test.py](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/test.py)** - A simple API test script
2. **[api_test_detailed.py](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/api_test_detailed.py)** - A comprehensive test script with detailed output
3. **[run_test.bat](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/run_test.bat)** - Windows batch file to run the simple test
4. **[run_test.sh](file:///c%3A/strategy_test/PythonLearning/python_backend_structure/run_test.sh)** - Shell script to run the simple test

## 🚀 Prerequisites

1. Make sure the FastAPI server is running on `http://localhost:8000`
2. The `requests` Python library should be installed:
   ```bash
   pip install requests
   ```

## ▶️ Running the Tests

### Option 1: Simple Test Script
```bash
# On Windows
python test.py

# Or use the batch file
run_test.bat

# On Linux/Mac
python test.py

# Or use the shell script
./run_test.sh
```

### Option 2: Detailed Test Script
```bash
python api_test_detailed.py
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

Note: The test scripts are designed to be run multiple times without causing conflicts.

## 🛠️ Customization

You can modify the test scripts to:

1. Change the base URL by modifying the `BASE_URL` variable
2. Use different test user data by modifying the `TEST_USER` dictionary
3. Add additional test cases for other endpoints
4. Adjust timeout values in the detailed test script

## 📊 Test Output

The simple test script provides basic pass/fail information, while the detailed test script provides:

- Detailed error messages
- Test execution summary
- Number of passed/failed tests
- Timing information

## ⚠️ Troubleshooting

### Server Not Running
If you get connection errors, make sure the FastAPI server is running:
```bash
# If using Docker
docker-compose up

# If running directly
uvicorn app.main:app --reload
```

### Permission Issues
On Linux/Mac, make sure the shell script is executable:
```bash
chmod +x run_test.sh
```

### Missing Dependencies
If you get import errors, install the required dependencies:
```bash
pip install requests
```

## 🧪 Integration with CI/CD

These test scripts can be integrated into CI/CD pipelines to automatically verify API functionality during deployment processes.