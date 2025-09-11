import os
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
import sys
from unittest.mock import MagicMock
sys.modules['app.database'] = MagicMock()

from app.data import shared_data
from app.main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

print("Initial state:")
print(f"Total tables: {len(shared_data.sample_tables)}")
print(f"Occupied tables: {len([t for t in shared_data.sample_tables if t.is_occupied])}")

# Test the endpoint directly
response = client.get("/api/tables/occupied/")
print(f"API response status: {response.status_code}")
print(f"API response data: {response.json()}")
print(f"API response length: {len(response.json())}")