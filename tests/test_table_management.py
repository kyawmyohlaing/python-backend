import pytest
import os
from fastapi.testclient import TestClient
import copy

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
from app.models.table import TableResponse
from datetime import datetime

# Override the database dependency
app.dependency_overrides = {}

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

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Setup and teardown for each test"""
    # Store original data (deep copy to avoid reference issues)
    original_tables = copy.deepcopy(shared_data.sample_tables)
    original_orders = copy.deepcopy(shared_data.sample_orders)
    
    # Clear data for testing
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    yield
    
    # Restore original data
    shared_data.sample_tables.clear()
    shared_data.sample_tables.extend(original_tables)
    shared_data.sample_orders.clear()
    shared_data.sample_orders.extend(original_orders)

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

def test_create_table():
    """Test creating a new table"""
    response = client.post("/api/tables/", json=test_table_data)
    assert response.status_code == 200
    data = response.json()
    assert data["table_number"] == test_table_data["table_number"]
    assert data["capacity"] == test_table_data["capacity"]
    assert data["status"] == "available"
    assert len(data["seats"]) == test_table_data["capacity"]
    # Verify all seats are initialized correctly
    for i, seat in enumerate(data["seats"]):
        assert seat["seat_number"] == i + 1
        assert seat["status"] == "available"
        assert seat["customer_name"] is None

def test_get_tables():
    """Test getting all tables"""
    # Create a table first
    create_test_table()
    
    response = client.get("/api/tables/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert isinstance(data, list)

def test_get_table():
    """Test getting a specific table"""
    # Create a table first
    table = create_test_table()
    table_id = table["id"]
    table_number = table["table_number"]  # Get the actual table number
    
    response = client.get(f"/api/tables/{table_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == table_id
    assert data["table_number"] == table_number  # Use the actual table number

def test_get_nonexistent_table():
    """Test getting a nonexistent table"""
    response = client.get("/api/tables/99999")
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_update_table():
    """Test updating a table"""
    # Create a table first
    table = create_test_table()
    table_id = table["id"]
    
    update_data = {
        "capacity": 6
    }
    
    response = client.put(f"/api/tables/{table_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["capacity"] == 6
    assert len(data["seats"]) == 6

def test_update_table_number():
    """Test updating table number"""
    # Create a table first
    table = create_test_table()
    table_id = table["id"]
    original_table_number = table["table_number"]  # Get the actual table number
    
    update_data = {
        "table_number": original_table_number + 1  # Use a different number
    }
    
    response = client.put(f"/api/tables/{table_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["table_number"] == original_table_number + 1

def test_update_nonexistent_table():
    """Test updating a nonexistent table"""
    update_data = {
        "capacity": 6
    }
    
    response = client.put("/api/tables/99999", json=update_data)
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_delete_table():
    """Test deleting a table"""
    # Create a table first
    table = create_test_table()
    table_id = table["id"]
    
    response = client.delete(f"/api/tables/{table_id}")
    assert response.status_code == 200
    assert "message" in response.json()

def test_delete_nonexistent_table():
    """Test deleting a nonexistent table"""
    response = client.delete("/api/tables/99999")
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_delete_occupied_table():
    """Test deleting an occupied table (should fail)"""
    # Create a table and assign it to an order
    table = create_test_table()
    table_id = table["id"]
    
    order = create_test_order()
    order_id = order["id"]
    
    # Assign table to order
    client.post(f"/api/tables/{table_id}/assign/{order_id}")
    
    # Try to delete the occupied table
    response = client.delete(f"/api/tables/{table_id}")
    assert response.status_code == 400
    assert "Cannot delete an occupied table" in response.json()["detail"]

def test_assign_table_to_order():
    """Test assigning a table to an order"""
    # Create a table and an order
    table = create_test_table()
    table_id = table["id"]
    
    order = create_test_order()
    order_id = order["id"]
    
    response = client.post(f"/api/tables/{table_id}/assign/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["is_occupied"] == True
    assert data["current_order_id"] == order_id
    assert data["status"] == "occupied"
    # Verify all seats are marked as occupied
    for seat in data["seats"]:
        assert seat["status"] == "occupied"

def test_assign_table_to_nonexistent_order():
    """Test assigning a table to a nonexistent order"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    response = client.post(f"/api/tables/{table_id}/assign/99999")
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]

def test_assign_nonexistent_table():
    """Test assigning a nonexistent table to an order"""
    order = create_test_order()
    order_id = order["id"]
    
    response = client.post(f"/api/tables/99999/assign/{order_id}")
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_assign_occupied_table():
    """Test assigning an already occupied table (should fail)"""
    # Create a table and assign it to an order
    table = create_test_table()
    table_id = table["id"]
    
    order = create_test_order()
    order_id = order["id"]
    
    # Assign table to order
    client.post(f"/api/tables/{table_id}/assign/{order_id}")
    
    # Create another order and try to assign the same table
    order2 = create_test_order()
    order2_id = order2["id"]
    
    response = client.post(f"/api/tables/{table_id}/assign/{order2_id}")
    assert response.status_code == 400
    assert "Table is already occupied" in response.json()["detail"]

def test_release_table():
    """Test releasing a table"""
    # Create a table and assign it to an order
    table = create_test_table()
    table_id = table["id"]
    
    order = create_test_order()
    order_id = order["id"]
    
    # Assign table to order
    client.post(f"/api/tables/{table_id}/assign/{order_id}")
    
    # Release the table
    response = client.post(f"/api/tables/{table_id}/release")
    assert response.status_code == 200
    data = response.json()
    assert data["is_occupied"] == False
    assert data["current_order_id"] is None
    assert data["status"] == "available"
    # Verify all seats are marked as available
    for seat in data["seats"]:
        assert seat["status"] == "available"
        assert seat["customer_name"] is None

def test_release_nonexistent_table():
    """Test releasing a nonexistent table"""
    response = client.post("/api/tables/99999/release")
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_assign_seat():
    """Test assigning a specific seat"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    # Assign a seat
    response = client.post(f"/api/tables/{table_id}/assign-seat/1?customer_name=John Doe")
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

def test_assign_nonexistent_seat():
    """Test assigning a nonexistent seat"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    # Try to assign a seat that doesn't exist
    response = client.post(f"/api/tables/{table_id}/assign-seat/99?customer_name=John Doe")
    assert response.status_code == 404
    assert "Seat not found" in response.json()["detail"]

def test_release_seat():
    """Test releasing a specific seat"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    # Assign a seat first
    client.post(f"/api/tables/{table_id}/assign-seat/1?customer_name=John Doe")
    
    # Release the seat
    response = client.post(f"/api/tables/{table_id}/release-seat/1")
    assert response.status_code == 200
    data = response.json()
    assert "Seat 1 released successfully" in data["message"]
    
    # Verify the seat status
    table_response = client.get(f"/api/tables/{table_id}")
    table_data = table_response.json()
    seat = next((s for s in table_data["seats"] if s["seat_number"] == 1), None)
    assert seat is not None
    assert seat["status"] == "available"
    assert seat["customer_name"] is None

def test_release_nonexistent_seat():
    """Test releasing a nonexistent seat"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    # Try to release a seat that doesn't exist
    response = client.post(f"/api/tables/{table_id}/release-seat/99")
    assert response.status_code == 404
    assert "Seat not found" in response.json()["detail"]

def test_merge_tables():
    """Test merging two tables"""
    # Create two tables
    table1 = create_test_table()
    table1_id = table1["id"]
    
    table2_data = {
        "table_number": 100,
        "capacity": 2
    }
    response2 = client.post("/api/tables/", json=table2_data)
    table2 = response2.json()
    table2_id = table2["id"]
    
    # Create two orders
    order1 = create_test_order()
    order1_id = order1["id"]
    
    order2_data = {
        "order": [
            {"name": "Pizza", "price": 14.99, "category": "Main Course"},
            {"name": "Soda", "price": 2.99, "category": "Drinks"}
        ],
        "total": 17.98
    }
    response_order2 = client.post("/api/orders/", json=order2_data)
    order2 = response_order2.json()
    order2_id = order2["id"]
    
    # Assign tables to orders
    client.post(f"/api/tables/{table1_id}/assign/{order1_id}")
    client.post(f"/api/tables/{table2_id}/assign/{order2_id}")
    
    # Merge tables
    response = client.post(f"/api/tables/merge-tables/{table1_id}/{table2_id}")
    assert response.status_code == 200
    data = response.json()
    # After merge, table1 should have increased capacity
    assert data["capacity"] >= table1["capacity"] + table2["capacity"]

def test_merge_nonexistent_tables():
    """Test merging nonexistent tables"""
    response = client.post("/api/tables/merge-tables/99999/88888")
    assert response.status_code == 404
    assert "One or both tables not found" in response.json()["detail"]

def test_split_bill():
    """Test splitting a bill at a table"""
    # Create a table
    table = create_test_table()
    table_id = table["id"]
    
    # Create an order with multiple items
    order_data = {
        "order": [
            {"name": "Burger", "price": 8.99, "category": "Main Course"},
            {"name": "Fries", "price": 3.99, "category": "Sides"},
            {"name": "Soda", "price": 2.99, "category": "Drinks"}
        ],
        "total": 15.97
    }
    response_order = client.post("/api/orders/", json=order_data)
    order = response_order.json()
    order_id = order["id"]
    
    # Assign table to order
    client.post(f"/api/tables/{table_id}/assign/{order_id}")
    
    # Split the bill
    split_details = {
        "split_1": [0],  # First item (Burger)
        "split_2": [1, 2]  # Second and third items (Fries and Soda)
    }
    
    response = client.post(f"/api/tables/split-bill/{table_id}", json=split_details)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2  # Two new orders created

def test_split_bill_nonexistent_table():
    """Test splitting a bill for a nonexistent table"""
    split_details = {
        "split_1": [0],
        "split_2": [1]
    }
    
    response = client.post("/api/tables/split-bill/99999", json=split_details)
    assert response.status_code == 404
    assert "Table not found" in response.json()["detail"]

def test_get_available_tables():
    """Test getting available tables"""
    # Create a table
    create_test_table()
    
    response = client.get("/api/tables/available/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # At least one table should be available
    assert len(data) >= 1

def test_get_occupied_tables():
    """Test getting occupied tables"""
    # Clear tables to ensure we start with a clean state
    from app.data import shared_data
    shared_data.sample_tables.clear()
    
    # Add a few available tables
    shared_data.sample_tables.extend([
        TableResponse(
            id=1,
            table_number=1,
            capacity=4,
            is_occupied=False,
            current_order_id=None,
            status="available",
            seats=[]
        ),
        TableResponse(
            id=2,
            table_number=2,
            capacity=2,
            is_occupied=False,
            current_order_id=None,
            status="available",
            seats=[]
        )
    ])
    
    response = client.get("/api/tables/occupied/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # No tables should be occupied initially

def test_table_number_uniqueness():
    """Test that table numbers must be unique"""
    # Create a table
    create_test_table()
    
    # Try to create another table with the same number
    response = client.post("/api/tables/", json=test_table_data)
    assert response.status_code == 400
    assert "Table number already exists" in response.json()["detail"]