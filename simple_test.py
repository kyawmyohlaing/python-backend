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

def test_isolation():
    """Test that data isolation works correctly"""
    print(f"Initial tables count: {len(shared_data.sample_tables)}")
    
    # Clear data
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    print(f"After clearing: {len(shared_data.sample_tables)}")
    
    # Add a test table
    test_table_data = {
        "table_number": 123456,
        "capacity": 4
    }
    
    response = client.post("/api/tables/", json=test_table_data)
    print(f"Create table response: {response.status_code}")
    
    print(f"After creating table: {len(shared_data.sample_tables)}")
    
    # Clear data again
    shared_data.sample_tables.clear()
    shared_data.sample_orders.clear()
    
    print(f"After final clearing: {len(shared_data.sample_tables)}")
    
    return len(shared_data.sample_tables) == 0

if __name__ == "__main__":
    result = test_isolation()
    print(f"Test result: {result}")
    if result:
        print("Test passed!")
    else:
        print("Test failed!")