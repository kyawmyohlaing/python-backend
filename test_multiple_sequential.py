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

test_order_data = {
    "order": [
        {"name": "Burger", "price": 8.99, "category": "Main Course"},
        {"name": "Fries", "price": 3.99, "category": "Sides"}
    ],
    "total": 12.98
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

def create_test_order():
    """Helper function to create a test order"""
    response = client.post("/api/orders/", json=test_order_data)
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
        
        print("test_get_table passed!")
        return True
        
    except Exception as e:
        print(f"test_get_table failed with exception: {e}")
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

def test_update_table():
    """Test updating a table"""
    print("\n=== Starting test_update_table ===")
    
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
        
        update_data = {
            "capacity": 6
        }
        
        response = client.put(f"/api/tables/{table_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["capacity"] == 6
        assert len(data["seats"]) == 6
        
        print("test_update_table passed!")
        return True
        
    except Exception as e:
        print(f"test_update_table failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        try:
            next(setup_gen)  # Execute teardown part
        except StopIteration:
            pass  # Expected as generator is exhausted
    
    print("=== Finished test_update_table ===\n")

def test_delete_table():
    """Test deleting a table"""
    print("\n=== Starting test_delete_table ===")
    
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
        
        response = client.delete(f"/api/tables/{table_id}")
        assert response.status_code == 200
        assert "message" in response.json()
        
        print("test_delete_table passed!")
        return True
        
    except Exception as e:
        print(f"test_delete_table failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        try:
            next(setup_gen)  # Execute teardown part
        except StopIteration:
            pass  # Expected as generator is exhausted
    
    print("=== Finished test_delete_table ===\n")

if __name__ == "__main__":
    print("Running multiple tests sequentially...")
    
    # Run tests in sequence
    results = []
    results.append(test_get_table())
    results.append(test_update_table())
    results.append(test_delete_table())
    
    # Check results
    passed = sum(results)
    total = len(results)
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed!")
        exit(1)