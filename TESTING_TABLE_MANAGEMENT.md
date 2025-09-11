# Testing Table & Seat Management Features

## Overview
This document explains how to test the Table & Seat Management features implemented for the restaurant POS system. Multiple test suites are available to verify different aspects of the functionality.

## Test Suites

### 1. Backend API Tests (`tests/test_table_management.py`)
Comprehensive test suite for all table and seat management API endpoints using pytest.

### 2. Route Verification (`verify_table_routes.py`)
Simple script to verify that all table management routes are properly defined.

### 3. Test Runner (`run_table_tests.py`)
Convenience script to run table management tests.

## Prerequisites

### For Real API Tests
1. Docker and Docker Compose installed
2. Backend services running (`make dev`)
3. Python 3.11+ installed
4. pytest installed (`pip install pytest`)

### For Route Verification
1. Python 3.11+ installed
2. No backend services required

## Running Tests

### All Table Management Tests
```bash
# Using the test runner script
python run_table_tests.py

# Using Make (if in the backend directory)
make test-tables
```

### Individual Test Suites
```bash
# Run with pytest directly
pytest tests/test_table_management.py -v

# Verify route definitions only
python verify_table_routes.py
```

## Test Categories

### 1. Table CRUD Operations
- `test_create_table()` - Create new tables
- `test_get_tables()` - Fetch all tables
- `test_get_table()` - Fetch specific tables
- `test_update_table()` - Update table properties
- `test_delete_table()` - Delete tables
- `test_table_number_uniqueness()` - Validate unique table numbers

### 2. Table Assignment
- `test_assign_table_to_order()` - Assign tables to orders
- `test_release_table()` - Release tables from orders
- `test_assign_occupied_table()` - Prevent double assignment
- `test_delete_occupied_table()` - Prevent deletion of occupied tables

### 3. Seat Management
- `test_assign_seat()` - Assign individual seats
- `test_release_seat()` - Release individual seats
- `test_assign_nonexistent_seat()` - Handle invalid seats
- `test_release_nonexistent_seat()` - Handle invalid seats

### 4. Merge/Split Functionality
- `test_merge_tables()` - Merge two tables
- `test_split_bill()` - Split bills at tables
- `test_merge_nonexistent_tables()` - Handle invalid tables
- `test_split_bill_nonexistent_table()` - Handle invalid tables

### 5. Table Status Queries
- `test_get_available_tables()` - Fetch available tables
- `test_get_occupied_tables()` - Fetch occupied tables

### 6. Error Handling
- `test_get_nonexistent_table()` - Handle missing tables
- `test_update_nonexistent_table()` - Handle missing tables
- `test_delete_nonexistent_table()` - Handle missing tables
- `test_assign_nonexistent_table()` - Handle missing tables

## Test Data Management

### Automatic Cleanup
- Each test runs in isolation
- Fixtures automatically set up and tear down test data
- No residual test data remains after tests complete

### Test Data Creation
- Tables are created with unique table numbers (e.g., 99, 100)
- Orders are created with realistic menu items
- Seats are assigned with customer names for tracking

## Expected Test Output

### Success
```
============================= test session starts =============================
collected 25 items

tests/test_table_management.py::test_create_table PASSED              [  4%]
tests/test_table_management.py::test_get_tables PASSED                [  8%]
tests/test_table_management.py::test_get_table PASSED                 [ 12%]
...
tests/test_table_management.py::test_get_occupied_tables PASSED       [100%]

============================= 25 passed in 3.24s ==============================
```

### Failure
```
tests/test_table_management.py::test_create_table FAILED              [  4%]
E   assert response.status_code == 200
E   AssertionError: Expected 200 but got 500
```

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```
OperationalError: could not translate host name "db" to address
```
**Solution:** Start the backend services with `make dev` before running tests.

#### 2. pytest Not Found
```
ModuleNotFoundError: No module named 'pytest'
```
**Solution:** Install pytest with `pip install pytest`.

#### 3. Import Errors
```
ModuleNotFoundError: No module named 'app'
```
**Solution:** Run tests from the backend directory root.

### Debugging Tips

1. **Run individual tests** to isolate specific failures:
   ```bash
   pytest tests/test_table_management.py::test_create_table -v
   ```

2. **Check backend logs** for detailed error messages:
   ```bash
   make logs
   ```

3. **Verify route definitions** without running the full test suite:
   ```bash
   python verify_table_routes.py
   ```

## Continuous Integration

### GitHub Actions Setup
```yaml
name: Table Management Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest
    - name: Start services
      run: make dev
    - name: Run table management tests
      run: python run_table_tests.py
```

## Test Coverage

### Currently Tested Features
- [x] Table CRUD operations
- [x] Table assignment/release
- [x] Seat assignment/release
- [x] Merge tables functionality
- [x] Split bill functionality
- [x] Table status queries
- [x] Error handling
- [x] Data cleanup

### Future Test Enhancements
- [ ] Performance tests
- [ ] Load testing
- [ ] Security tests
- [ ] Integration with other modules

## Best Practices

### Writing New Tests
1. Use the existing test patterns
2. Include both positive and negative test cases
3. Use descriptive test names
4. Clean up test data in fixtures

### Running Tests in CI/CD
1. Ensure backend services are running
2. Set up proper test reporting
3. Fail builds on test failures
4. Run tests in isolated environments

## Extending Tests

### Adding New Test Cases
1. Add new test functions to `tests/test_table_management.py`
2. Follow the existing pattern for setup/teardown
3. Include comprehensive error handling
4. Update documentation

### Modifying Existing Tests
1. Ensure backward compatibility
2. Test changes thoroughly
3. Maintain consistent output format
4. Update documentation when changing behavior