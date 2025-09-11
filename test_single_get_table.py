import pytest
import os
from fastapi.testclient import TestClient

# Set environment variables before importing anything
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
import sys
from unittest.mock import MagicMock

# Mock the database module
sys.modules['app.database'] = MagicMock()

# Now import the app and other modules
from app.main import app
from app.data import shared_data

# Create a test client
client = TestClient(app)

# Test data
test_table_data = {
    "table_number": 99,
    "capacity": 4
}

def setup_and_teardown():
    """Setup and teardown for each test"""
    print("Setup: Storing original data")
    # Store original data
    original_tables = shared_data.sample_tables.copy()
    original_orders = shared_data.sample_orders.copy()
    
    print(f"Setup: Original tables count: {len(original_tables)}")
    print(f"Setup: Current tables count: {len(shared_data.sample_tables)}")
    
    # Clear data for testing
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    print(f"Setup: After clear, tables count: {len(shared_data.sample_tables)}")
    
    yield
    
    print("Teardown: Restoring original data")
    # Restore original data
    shared_data.sample_tables.clear()
    shared_data.sample_tables.extend(original_tables)
    shared_data.sample_orders.clear()
    shared_data.sample_orders.extend(original_orders)
    print(f"Teardown: Tables count after restore: {len(shared_data.sample_tables)}")

def create_test_table():
    """Helper function to create a test table"""
    response = client.post("/api/tables/", json=test_table_data)
    return response.json()

def test_get_table():
    """Test getting a specific table"""
    print("\n=== Starting test_get_table ===")
    
    # Setup
    setup_gen = setup_and_teardown()
    next(setup_gen)  # Execute setup part
    
    try:
        # Create a table first
        table = create_test_table()
        print(f"Created table: {table}")
        
        # Check if table has id
        if "id" not in table:
            raise KeyError("Table does not have 'id' key")
            
        table_id = table["id"]
        print(f"Table ID: {table_id}")
        
        response = client.get(f"/api/tables/{table_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == table_id
        assert data["table_number"] == test_table_data["table_number"]
        
        print("Test passed!")
        return True
        
    except Exception as e:
        print(f"Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        try:
            next(setup_gen)  # Execute teardown part
        except StopIteration:
            pass  # Expected as generator is exhausted
    
    print("=== Finished test_get_table ===\n")

if __name__ == "__main__":
    success = test_get_table()
    exit(0 if success else 1)