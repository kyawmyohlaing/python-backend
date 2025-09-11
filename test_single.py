import os
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
import sys
from unittest.mock import MagicMock
sys.modules['app.database'] = MagicMock()

from app.main import app
from app.data import shared_data
from fastapi.testclient import TestClient
import copy

# Create a test client
client = TestClient(app)

def setup_and_teardown():
    """Setup and teardown for each test"""
    # Clear data for testing (start with clean state)
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    shared_data.sample_kitchen_orders.clear()
    
    yield
    
    # Clear data after test
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    shared_data.sample_kitchen_orders.clear()

def test_get_occupied_tables():
    """Test getting occupied tables"""
    # Debug: Print the current state of tables
    print(f"Number of tables before test: {len(shared_data.sample_tables)}")
    for i, table in enumerate(shared_data.sample_tables):
        print(f"Table {i}: id={table.id}, is_occupied={table.is_occupied}")
    
    # Initially, no tables should be occupied
    response = client.get("/api/tables/occupied/")
    print(f"Response status: {response.status_code}")
    data = response.json()
    print(f"Number of occupied tables returned: {len(data)}")
    print(f"Response data: {data}")
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

# Run the setup
gen = setup_and_teardown()
next(gen)  # This is equivalent to running the code before yield

# Run the test
try:
    test_get_occupied_tables()
    print("Test passed!")
except Exception as e:
    print(f"Test failed with error: {e}")

# Run the teardown
try:
    next(gen)  # This should raise StopIteration
except StopIteration:
    pass  # This is expected