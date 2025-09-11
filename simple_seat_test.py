import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple test to check seat assignment
from app.data.shared_data import sample_tables

print("Before assignment:")
table = sample_tables[0]
print(f"Table status: {table.status}")
print(f"Is occupied: {table.is_occupied}")
if table.seats is not None:
    for i, seat in enumerate(table.seats):
        print(f"Seat {i+1}: {seat}")
else:
    print("No seats available")

# Check if table.seats is not None before accessing it
if table.seats is not None and len(table.seats) > 0:
    # Manually assign a seat
    seat = table.seats[0]  # First seat
    seat["status"] = "occupied"
    seat["customer_name"] = "John Doe"

    # Update table status if needed
    if not table.is_occupied:
        table.is_occupied = True
        table.status = "occupied"
else:
    print("Error: table.seats is None or empty")

print("\nAfter assignment:")
print(f"Table status: {table.status}")
print(f"Is occupied: {table.is_occupied}")
if table.seats is not None:
    for i, seat in enumerate(table.seats):
        print(f"Seat {i+1}: {seat}")
else:
    print("No seats available")