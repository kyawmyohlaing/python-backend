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

def create_test_table():
    """Helper function to create a test table"""
    response = client.post("/api/tables/", json=test_table_data)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        # If there's an error (like table number already exists), 
        # create a table with a unique table number
        unique_table_data = test_table_data.copy()
        # Use a unique table number based on current time
        import time
        unique_table_data["table_number"] = int(time.time()) % 1000000
        response = client.post("/api/tables/", json=unique_table_data)
        return response.json()

if __name__ == "__main__":
    print("Testing create_test_table function...")
    
    # Clear any existing data
    shared_data.sample_tables.clear()
    
    # Create first table
    print("Creating first table...")
    table1 = create_test_table()
    print(f"First table: {table1}")
    print(f"Has 'id' key: {'id' in table1}")
    
    # Create second table (should use unique number)
    print("Creating second table...")
    table2 = create_test_table()
    print(f"Second table: {table2}")
    print(f"Has 'id' key: {'id' in table2}")
    
    # Check that both tables have IDs
    if "id" in table1 and "id" in table2:
        print("SUCCESS: Both tables have IDs")
        exit(0)
    else:
        print("FAILURE: One or both tables missing IDs")
        exit(1)