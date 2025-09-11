import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.data.shared_data import sample_tables, sample_orders
from app.routes.table_routes import (
    get_tables, create_table, get_table, update_table, delete_table,
    assign_table_to_order, release_table, assign_seat, release_seat,
    get_occupied_tables, get_available_tables
)
from app.models.table import TableCreate, TableUpdate

def test_table_management():
    print("=== Table Management Functionality Test ===\n")
    
    # Test 1: Get all tables
    print("1. Getting all tables...")
    tables = get_tables()
    print(f"   Found {len(tables)} tables\n")
    
    # Test 2: Create a new table
    print("2. Creating a new table...")
    table_create = TableCreate(table_number=5, capacity=4)
    new_table = create_table(table_create)
    print(f"   Created table {new_table.id} with number {new_table.table_number} and capacity {new_table.capacity}")
    seat_count = len(new_table.seats) if new_table.seats is not None else 0
    print(f"   Seats: {seat_count}\n")
    
    # Test 3: Get specific table
    print("3. Getting specific table...")
    table = get_table(new_table.id)
    print(f"   Retrieved table {table.id} with status '{table.status}'\n")
    
    # Test 4: Update table
    print("4. Updating table...")
    table_update = TableUpdate(capacity=6)
    updated_table = update_table(new_table.id, table_update)
    print(f"   Updated table capacity to {updated_table.capacity}")
    seat_count = len(updated_table.seats) if updated_table.seats is not None else 0
    print(f"   Seats: {seat_count}\n")
    
    # Test 5: Assign seat
    print("5. Assigning seat...")
    try:
        result = assign_seat(new_table.id, 1, "John Doe")
        print(f"   {result}\n")
    except Exception as e:
        print(f"   Error assigning seat: {e}\n")
    
    # Test 6: Release seat
    print("6. Releasing seat...")
    try:
        result = release_seat(new_table.id, 1)
        print(f"   {result}\n")
    except Exception as e:
        print(f"   Error releasing seat: {e}\n")
    
    # Test 7: Get occupied tables
    print("7. Getting occupied tables...")
    occupied = get_occupied_tables()
    print(f"   Found {len(occupied)} occupied tables\n")
    
    # Test 8: Get available tables
    print("8. Getting available tables...")
    available = get_available_tables()
    print(f"   Found {len(available)} available tables\n")
    
    # Test 9: Delete table
    print("9. Deleting table...")
    try:
        result = delete_table(new_table.id)
        print(f"   {result}\n")
    except Exception as e:
        print(f"   Error deleting table: {e}\n")
    
    print("=== Test completed ===")

if __name__ == "__main__":
    test_table_management()