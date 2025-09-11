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

# Create a test client
client = TestClient(app)

print("=== Current State ===")
print(f"Number of tables: {len(shared_data.sample_tables)}")
print(f"Number of orders: {len(shared_data.sample_orders)}")

# Create an order first
print("\n=== Creating Order ===")
order_data = {
    "order": [
        {"name": "Burger", "price": 8.99, "category": "Main Course"},
        {"name": "Fries", "price": 3.99, "category": "Sides"}
    ],
    "total": 12.98
}

response = client.post("/api/orders/", json=order_data)
print(f"Create order response status: {response.status_code}")

if response.status_code == 200:
    order = response.json()
    order_id = order["id"]
    print(f"Created order with ID: {order_id}")
    
    # Now assign the order to a table
    print("\n=== Assigning Order to Table ===")
    table_id = 1  # Using the first table
    
    response = client.post(f"/api/tables/{table_id}/assign/{order_id}")
    print(f"Assign table response status: {response.status_code}")
    
    if response.status_code == 200:
        print("Successfully assigned order to table!")
        result = response.json()
        print(f"Table status: {result['status']}")
        print(f"Is occupied: {result['is_occupied']}")
    else:
        print(f"Failed to assign table: {response.json()}")
else:
    print(f"Failed to create order: {response.json()}")

print("\n=== Final State ===")
print(f"Number of tables: {len(shared_data.sample_tables)}")
print(f"Number of orders: {len(shared_data.sample_orders)}")