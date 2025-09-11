# Table & Seat Management API Tests

## Overview
This document describes the test suite for the Table & Seat Management API endpoints. The tests verify that all table and seat management functionality works correctly in the restaurant POS system.

## Test File
The tests are implemented in `tests/test_table_management.py` and can be run using pytest or the provided test runner.

## Test Categories

### 1. Table CRUD Operations
- Create new tables with specified table numbers and capacities
- Fetch all tables
- Fetch specific tables by ID
- Update table properties (table number, capacity)
- Delete tables
- Validate table number uniqueness

### 2. Table Assignment
- Assign tables to orders
- Release tables from orders
- Verify table status changes (available → occupied → available)
- Prevent assignment of already occupied tables
- Prevent deletion of occupied tables

### 3. Seat Management
- Assign individual seats to customers
- Release individual seats
- Track seat status (available, occupied)
- Associate customer names with seats
- Handle nonexistent seats gracefully

### 4. Merge/Split Functionality
- Merge two tables into a single order
- Split a bill at a table into multiple orders
- Handle nonexistent tables gracefully

### 5. Table Status Queries
- Fetch available tables
- Fetch occupied tables
- Verify table status consistency

## Running the Tests

### Prerequisites
- Python 3.11+
- pytest installed (`pip install pytest`)
- FastAPI backend dependencies installed

### Running with pytest
```bash
# Run all table management tests
pytest tests/test_table_management.py -v

# Run a specific test
pytest tests/test_table_management.py::test_create_table -v
```

### Running with the test runner
```bash
# Run all table management tests
python run_table_tests.py
```

### Running with Make
```bash
# Run all table management tests
make test-tables
```

## Test Data Management

### Test Data Isolation
- Each test runs in isolation with a clean state
- Fixtures automatically set up and tear down test data
- No residual test data remains after tests complete

### Test Data Creation
- Tables are created with unique table numbers
- Orders are created for assignment testing
- Seats are assigned with customer names for tracking

## Test Scenarios

### Basic Table Operations
1. Create a new table with table number 99 and capacity 4
2. Fetch all tables and verify the new table is included
3. Fetch the specific table by ID
4. Update the table capacity from 4 to 6
5. Delete the table

### Table Assignment Flow
1. Create an order with multiple items
2. Assign a table to the order
3. Verify table status changes to "occupied"
4. Release the table
5. Verify table status changes to "available"

### Seat Management Flow
1. Assign seat 1 to customer "John Doe"
2. Assign seat 2 to customer "Jane Smith"
3. Release seat 1
4. Verify seat status changes appropriately

### Merge/Split Operations
1. Create two tables with different table numbers
2. Create two separate orders
3. Assign each table to a different order
4. Merge the tables (combine orders)
5. Split a bill (separate orders)

## Error Handling Tests

### Invalid Table IDs
- Attempting to fetch a nonexistent table
- Attempting to update a nonexistent table
- Attempting to delete a nonexistent table

### Invalid Seat Numbers
- Attempting to assign a seat that doesn't exist
- Attempting to release a seat that doesn't exist

### Invalid Operations
- Attempting to assign an already occupied table
- Attempting to delete an occupied table
- Attempting to merge unassigned tables

## Expected Results

### Success Cases
- All API calls return appropriate HTTP status codes
- Response data matches expected structure
- Table and seat statuses update correctly
- No data inconsistencies

### Error Cases
- Appropriate error messages are returned
- HTTP status codes match error types
- System state remains consistent

## Test Output

### Success Output
```
tests/test_table_management.py::test_create_table PASSED
tests/test_table_management.py::test_get_tables PASSED
tests/test_table_management.py::test_get_table PASSED
...
========================= 25 passed in 2.45s =========================
```

### Error Output
```
tests/test_table_management.py::test_assign_occupied_table FAILED
E   assert 400 == 200
E   AssertionError: Table should be occupied after assignment
```

## Integration with CI/CD

### GitHub Actions Setup
```yaml
name: Table Management API Tests
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
    - name: Run table management tests
      run: python run_table_tests.py
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest'
                sh 'python run_table_tests.py'
            }
        }
    }
}
```

## Extending the Tests

### Adding New Test Cases
1. Add new test functions to `tests/test_table_management.py`
2. Follow the existing pattern for setup/teardown
3. Include both positive and negative test cases
4. Use descriptive test names

### Modifying Existing Tests
1. Update the relevant test function
2. Ensure backward compatibility
3. Test changes thoroughly

## Best Practices

### Test Data Isolation
- Use fixtures for automatic setup/teardown
- Avoid conflicts between tests
- Clean up all test data after testing

### Error Handling
- Test both success and failure cases
- Verify appropriate error messages
- Ensure system stability during errors

### Performance Considerations
- Minimize the number of API calls per test
- Reuse test data when possible
- Keep tests focused and fast