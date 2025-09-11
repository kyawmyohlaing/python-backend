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

print("=== Initial State ===")
table = shared_data.sample_tables[0]  # Get the first table
print(f"Table ID: {table.id}")
print(f"Table Status: {table.status}")
print(f"Is Occupied: {table.is_occupied}")
print("Seats:")
for i, seat in enumerate(table.seats):
    print(f"  Seat {i+1}: {seat}")

print("\n=== Assigning Seat 1 ===")
response = client.post("/api/tables/1/assign-seat/1", params={"customer_name": "John Doe"})
print(f"Response Status: {response.status_code}")
print(f"Response Data: {response.json()}")

print("\n=== State After Assignment ===")
table = shared_data.sample_tables[0]  # Get the first table again
print(f"Table ID: {table.id}")
print(f"Table Status: {table.status}")
print(f"Is Occupied: {table.is_occupied}")
print("Seats:")
for i, seat in enumerate(table.seats):
    print(f"  Seat {i+1}: {seat}")