import sys
import os

# Set environment variables before importing anything
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
from unittest.mock import MagicMock

# Mock the database module
sys.modules['app.database'] = MagicMock()

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
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

def setup_test():
    """Setup for each test - clear all data"""
    print(f"Before setup - Tables count: {len(shared_data.sample_tables)}")
    
    # Clear all data
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    print(f"After setup - Tables count: {len(shared_data.sample_tables)}")

def teardown_test():
    """Teardown for each test - clear all data"""
    print(f"Before teardown - Tables count: {len(shared_data.sample_tables)}")
    
    # Clear all data
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    print(f"After teardown - Tables count: {len(shared_data.sample_tables)}")

def create_test_table():
    """Helper function to create a test table"""
    # Generate a unique table number to avoid conflicts
    import random
    unique_table_data = test_table_data.copy()
    unique_table_data["table_number"] = random.randint(1000, 999999)
    
    response = client.post("/api/tables/", json=unique_table_data)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # If there's still an error, try one more time with a different number
        unique_table_data["table_number"] = random.randint(1000000, 9999999)
        response = client.post("/api/tables/", json=unique_table_data)
        return response.json()

def create_test_order():
    """Helper function to create a test order"""
    response = client.post("/api/orders/", json=test_order_data)
    return response.json()

def test_assign_table_to_nonexistent_order():
    """Test assigning a table to a nonexistent order"""
    print("Testing assign_table_to_nonexistent_order...")
    
    # Setup
    setup_test()
    
    try:
        # Create a table
        table = create_test_table()
        table_id = table["id"]
        print(f"Created table with ID: {table_id}")

        response = client.post(f"/api/tables/{table_id}/assign/99999")
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.json()}")
        assert response.status_code == 404
        assert "Order not found" in response.json()["detail"]
        
        print("test_assign_table_to_nonexistent_order passed!")
        return True
        
    except Exception as e:
        print(f"test_assign_table_to_nonexistent_order failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        teardown_test()

def test_assign_seat():
    """Test assigning a specific seat"""
    print("Testing assign_seat...")
    
    # Setup
    setup_test()
    
    try:
        # Create a table
        table = create_test_table()
        table_id = table["id"]
        print(f"Created table with ID: {table_id}")

        # Assign a seat
        response = client.post(f"/api/tables/{table_id}/assign-seat/1?customer_name=John Doe")
        print(f"Assign seat response status: {response.status_code}")
        print(f"Assign seat response data: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert "Seat 1 assigned successfully" in data["message"]

        # Verify the seat status
        table_response = client.get(f"/api/tables/{table_id}")
        table_data = table_response.json()
        seat = next((s for s in table_data["seats"] if s["seat_number"] == 1), None)
        assert seat is not None
        assert seat["status"] == "occupied"
        assert seat["customer_name"] == "John Doe"
        
        print("test_assign_seat passed!")
        return True
        
    except Exception as e:
        print(f"test_assign_seat failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        teardown_test()

def test_get_occupied_tables():
    """Test getting occupied tables"""
    print("Testing get_occupied_tables...")
    
    # Setup
    setup_test()
    
    try:
        print(f"Current tables in shared_data: {len(shared_data.sample_tables)}")
        for table in shared_data.sample_tables:
            print(f"  Table ID: {table.id}, Table Number: {table.table_number}, Occupied: {table.is_occupied}")
        
        # Initially, no tables should be occupied
        response = client.get("/api/tables/occupied/")
        print(f"Get occupied tables response status: {response.status_code}")
        print(f"Get occupied tables response data: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # This should now pass
        
        print("test_get_occupied_tables passed!")
        return True
        
    except Exception as e:
        print(f"test_get_occupied_tables failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Teardown
        teardown_test()

if __name__ == "__main__":
    print("Running fix verification tests...")
    
    # Run tests
    results = []
    results.append(test_assign_table_to_nonexistent_order())
    results.append(test_assign_seat())
    results.append(test_get_occupied_tables())
    
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