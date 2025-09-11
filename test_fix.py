import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables before importing anything
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
from unittest.mock import MagicMock

# Mock the database module
import sys
sys.modules['app.database'] = MagicMock()

# Now import the app and other modules
from app.routes.table_routes import assign_table_to_order
from fastapi import HTTPException

# Test the function
try:
    # This should raise an HTTPException with status_code 404
    assign_table_to_order(1, 99999)
    print("ERROR: Function should have raised an exception")
except HTTPException as e:
    if e.status_code == 404 and "Order not found" in str(e.detail):
        print("SUCCESS: Function correctly raises 404 for nonexistent order")
    else:
        print(f"ERROR: Unexpected exception: {e}")
except Exception as e:
    print(f"ERROR: Unexpected exception type: {e}")