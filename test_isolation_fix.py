import sys
import os
import copy

# Set environment variables before importing anything
os.environ["ENVIRONMENT"] = "testing"
os.environ["TEST_DATABASE_URL"] = "sqlite:///./test.db"

# Mock the database dependency to avoid connection issues
from unittest.mock import MagicMock

# Mock the database module
sys.modules['app.database'] = MagicMock()

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app.data import shared_data
from app.models.table import TableResponse

def test_deep_copy_fix():
    """Test that deep copy properly isolates table objects"""
    print("Initial tables count:", len(shared_data.sample_tables))
    
    # Store original data with deep copy
    original_tables = copy.deepcopy(shared_data.sample_tables)
    print("Stored original tables count:", len(original_tables))
    
    # Modify a table in the shared data
    if shared_data.sample_tables:
        table = shared_data.sample_tables[0]
        print(f"Before modification - Table {table.id} occupied: {table.is_occupied}")
        table.is_occupied = True
        print(f"After modification - Table {table.id} occupied: {table.is_occupied}")
    
    # Check if the original copy was affected
    if original_tables:
        original_table = original_tables[0]
        print(f"Original copy - Table {original_table.id} occupied: {original_table.is_occupied}")
        
        # Restore original data
        shared_data.sample_tables.clear()
        shared_data.sample_tables.extend(original_tables)
        
        # Check if the table is back to original state
        if shared_data.sample_tables:
            restored_table = shared_data.sample_tables[0]
            print(f"Restored table - Table {restored_table.id} occupied: {restored_table.is_occupied}")
            
            return not restored_table.is_occupied  # Should be False if fix works
    
    return False

if __name__ == "__main__":
    result = test_deep_copy_fix()
    print(f"Test result: {result}")
    if result:
        print("Deep copy fix works correctly!")
    else:
        print("Deep copy fix failed!")