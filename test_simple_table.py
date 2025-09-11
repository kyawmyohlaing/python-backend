import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from fastapi.testclient import TestClient
from app.main import app

# Create a test client
client = TestClient(app)

def test_create_table():
    """Test creating a new table"""
    test_table_data = {
        "table_number": 99,
        "capacity": 4
    }
    
    response = client.post("/api/tables/", json=test_table_data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"ID: {data.get('id')}")
        print(f"Table number: {data.get('table_number')}")
        print(f"Capacity: {data.get('capacity')}")
        return True
    else:
        print(f"Error: {response.json()}")
        return False

if __name__ == "__main__":
    print("Testing table creation...")
    success = test_create_table()
    if success:
        print("Test passed!")
    else:
        print("Test failed!")