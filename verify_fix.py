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

# Import the modules
from app.data.shared_data import sample_tables, sample_orders
from app.routes.table_routes import assign_table_to_order
from fastapi import HTTPException

print("=== Testing Fixes ===")

# Test 1: Check that sample_tables is properly initialized
print(f"1. Number of sample tables: {len(sample_tables)}")
for i, table in enumerate(sample_tables):
    print(f"   Table {i+1}: ID={table.id}, Number={table.table_number}, Seats={table.seats}")

# Test 2: Check that sample_orders is properly initialized
print(f"2. Number of sample orders: {len(sample_orders)}")

# Test 3: Test assign_table_to_order with nonexistent order
print("3. Testing assign_table_to_order with nonexistent order...")
try:
    # This should raise an HTTPException with status_code 404
    result = assign_table_to_order(1, 99999)
    print("   ERROR: Function should have raised an exception")
except HTTPException as e:
    if e.status_code == 404 and "Order not found" in str(e.detail):
        print("   SUCCESS: Function correctly raises 404 for nonexistent order")
    else:
        print(f"   ERROR: Unexpected exception: {e.detail} (status {e.status_code})")
except Exception as e:
    print(f"   ERROR: Unexpected exception type: {type(e).__name__}: {e}")

print("=== Test Complete ===")