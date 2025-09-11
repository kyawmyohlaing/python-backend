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

print("=== Debug Information ===")
print(f"Number of tables in shared_data: {len(shared_data.sample_tables)}")
print("Table details:")
for i, table in enumerate(shared_data.sample_tables):
    print(f"  Table {i+1}: id={table.id}, table_number={table.table_number}, is_occupied={table.is_occupied}")

print("\n=== Testing /api/tables/occupied/ endpoint ===")
response = client.get("/api/tables/occupied/")
print(f"Response status: {response.status_code}")
print(f"Response data: {response.json()}")
print(f"Number of occupied tables: {len(response.json())}")

print("\n=== Testing /api/tables/ endpoint ===")
response_all = client.get("/api/tables/")
print(f"Response status: {response_all.status_code}")
print(f"Number of total tables: {len(response_all.json())}")