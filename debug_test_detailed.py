import sys
import os
import pytest
from unittest.mock import MagicMock

# Set environment variables before importing anything
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database module
sys.modules['app.database'] = MagicMock()

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app
from app.data.shared_data import sample_tables, sample_orders

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
    original_tables = sample_tables.copy()
    original_orders = sample_orders.copy()
    
    print(f"Setup: Original tables count: {len(original_tables)}")
    print(f"Setup: Current tables count: {len(sample_tables)}")
    
    # Clear data for testing
    sample_tables.clear()
    sample_orders.clear()
    
    print(f"Setup: After clear, tables count: {len(sample_tables)}")
    
    yield
    
    print("Teardown: Restoring original data")
    # Restore original data
    sample_tables.clear()
    sample_tables.extend(original_tables)
    sample_orders.clear()
    sample_orders.extend(original_orders)
    print(f"Teardown: Tables count after restore: {len(sample_tables)}")

def create_test_table():
    """Helper function to create a test table"""
    print(f"Creating test table with data: {test_table_data}")
    response = client.post("/api/tables/", json=test_table_data)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")
    return response.json()

def test_get_table_detailed():
    """Test getting a specific table with detailed debugging"""
    print("\n=== Starting test_get_table_detailed ===")
    
    # Setup
    setup_gen = setup_and_teardown()
    next(setup_gen)  # Execute setup part
    
    try:
        print(f"Before create_test_table, tables count: {len(sample_tables)}")
        # Create a table first
        table = create_test_table()
        print(f"After create_test_table, tables count: {len(sample_tables)}")
        print(f"Created table: {table}")
        print(f"Table keys: {table.keys()}")
        print(f"Has 'id' key: {'id' in table}")
        
        if 'id' in table:
            table_id = table["id"]
            print(f"Table ID: {table_id}")
            
            response = client.get(f"/api/tables/{table_id}")
            print(f"Get table response status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Get table response data: {data}")
            else:
                print(f"Get table error response: {response.json()}")
        else:
            print("ERROR: Created table does not have 'id' key!")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Teardown
        try:
            next(setup_gen)  # Execute teardown part
        except StopIteration:
            pass  # Expected as generator is exhausted
    
    print("=== Finished test_get_table_detailed ===\n")

if __name__ == "__main__":
    test_get_table_detailed()