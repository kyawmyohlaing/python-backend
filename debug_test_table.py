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

# Create a test client
client = TestClient(app)

# Test data
test_table_data = {
    "table_number": 99,
    "capacity": 4
}

def create_test_table():
    """Helper function to create a test table"""
    response = client.post("/api/tables/", json=test_table_data)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("Debugging table creation...")
    table = create_test_table()
    print(f"Table object: {table}")
    print(f"Has 'id' key: {'id' in table}")
    if 'id' in table:
        print(f"ID value: {table['id']}")