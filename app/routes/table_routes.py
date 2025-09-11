from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.table import TableCreate, TableUpdate, TableResponse
from models.order import OrderResponse
from data.shared_data import sample_tables, sample_orders

router = APIRouter(prefix="/api/tables", tags=["Tables"])

@router.get("/", response_model=List[TableResponse])
def get_tables():
    """Get all tables"""
    return sample_tables

@router.get("/{table_id}", response_model=TableResponse)
def get_table(table_id: int):
    """Get a specific table by ID"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.post("/", response_model=TableResponse)
def create_table(table: TableCreate):
    """Create a new table"""
    # Check if table number already exists
    existing_table = next((t for t in sample_tables if t.table_number == table.table_number), None)
    if existing_table:
        raise HTTPException(status_code=400, detail="Table number already exists")
    
    # Initialize seats array with default values
    seats = [{"seat_number": i+1, "status": "available", "customer_name": None} for i in range(table.capacity)]
    
    new_id = len(sample_tables) + 1
    new_table = TableResponse(
        id=new_id,
        table_number=table.table_number,
        capacity=table.capacity,
        is_occupied=False,
        current_order_id=None,
        status="available",
        seats=seats
    )
    sample_tables.append(new_table)
    return new_table

@router.put("/{table_id}", response_model=TableResponse)
def update_table(table_id: int, table_update: TableUpdate):
    """Update a table"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Update table fields if provided
    if table_update.table_number is not None:
        # Check if new table number already exists (and it's not the current table)
        existing_table = next((t for t in sample_tables if t.table_number == table_update.table_number and t.id != table_id), None)
        if existing_table:
            raise HTTPException(status_code=400, detail="Table number already exists")
        table.table_number = table_update.table_number
    
    if table_update.capacity is not None:
        table.capacity = table_update.capacity
        # Update seats array to match new capacity
        # Ensure seats is not None before working with it
        if table.seats is None:
            table.seats = []
        
        if table_update.capacity > len(table.seats):
            # Add new seats
            for i in range(len(table.seats), table_update.capacity):
                table.seats.append({"seat_number": i+1, "status": "available", "customer_name": None})
        elif table_update.capacity < len(table.seats):
            # Remove extra seats
            table.seats = table.seats[:table_update.capacity]
    
    if table_update.is_occupied is not None:
        table.is_occupied = table_update.is_occupied
    
    if table_update.current_order_id is not None:
        table.current_order_id = table_update.current_order_id
    
    if table_update.status is not None:
        table.status = table_update.status
    
    if table_update.seats is not None:
        table.seats = table_update.seats
    
    return table

@router.delete("/{table_id}")
def delete_table(table_id: int):
    """Delete a table"""
    global sample_tables
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if table is occupied
    if table.is_occupied:
        raise HTTPException(status_code=400, detail="Cannot delete an occupied table")
    
    sample_tables = [t for t in sample_tables if t.id != table_id]
    return {"message": "Table deleted successfully"}

# Table assignment functions
@router.post("/{table_id}/assign/{order_id}", response_model=TableResponse)
def assign_table_to_order(table_id: int, order_id: int):
    """Assign a table to an order"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if order exists
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if table is already occupied
    if table.is_occupied:
        raise HTTPException(status_code=400, detail="Table is already occupied")
    
    # Update table status
    table.is_occupied = True
    table.current_order_id = order_id
    table.status = "occupied"
    
    # Mark all seats as occupied
    # Ensure seats is not None before iterating
    if table.seats is None:
        table.seats = []
    for seat in table.seats:
        seat["status"] = "occupied"
    
    return table

@router.post("/{table_id}/release", response_model=TableResponse)
def release_table(table_id: int):
    """Release a table (mark as available)"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Update table status
    table.is_occupied = False
    table.current_order_id = None
    table.status = "available"
    
    # Mark all seats as available
    # Ensure seats is not None before iterating
    if table.seats is None:
        table.seats = []
    for seat in table.seats:
        seat["status"] = "available"
        seat["customer_name"] = None
    
    return table

# Seat management functions
@router.post("/{table_id}/assign-seat/{seat_number}")
def assign_seat(table_id: int, seat_number: int, customer_name: str = ""):
    """Assign a specific seat at a table"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Ensure seats is not None before working with it
    if table.seats is None:
        table.seats = []
    
    # Find the seat
    seat = next((s for s in table.seats if s["seat_number"] == seat_number), None)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    # Update seat status
    seat["status"] = "occupied"
    seat["customer_name"] = customer_name if customer_name else None
    
    # If table is not marked as occupied, update it
    if not table.is_occupied:
        table.is_occupied = True
        table.status = "occupied"
    
    return {"message": f"Seat {seat_number} assigned successfully"}

@router.post("/{table_id}/release-seat/{seat_number}")
def release_seat(table_id: int, seat_number: int):
    """Release a specific seat at a table"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Ensure seats is not None before working with it
    if table.seats is None:
        table.seats = []
    
    # Find the seat
    seat = next((s for s in table.seats if s["seat_number"] == seat_number), None)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    # Update seat status
    seat["status"] = "available"
    seat["customer_name"] = None
    
    # Check if all seats are now available, if so, release the table
    if all(s["status"] == "available" for s in table.seats):
        table.is_occupied = False
        table.current_order_id = None
        table.status = "available"
    
    return {"message": f"Seat {seat_number} released successfully"}

# Merge/Split bill functions
@router.post("/merge-tables/{table_id_1}/{table_id_2}", response_model=TableResponse)
def merge_tables(table_id_1: int, table_id_2: int):
    """Merge two tables into one order"""
    table1 = next((t for t in sample_tables if t.id == table_id_1), None)
    table2 = next((t for t in sample_tables if t.id == table_id_2), None)
    
    if not table1 or not table2:
        raise HTTPException(status_code=404, detail="One or both tables not found")
    
    if not table1.is_occupied or not table2.is_occupied:
        raise HTTPException(status_code=400, detail="Both tables must be occupied to merge")
    
    # Get the orders for both tables
    order1 = next((o for o in sample_orders if o.id == table1.current_order_id), None)
    order2 = next((o for o in sample_orders if o.id == table2.current_order_id), None)
    
    if not order1 or not order2:
        raise HTTPException(status_code=404, detail="Orders not found for one or both tables")
    
    # Combine orders (in a real app, you might want to create a new order)
    # For simplicity, we'll merge into the first order
    combined_order_items = order1.order + order2.order
    combined_total = order1.total + order2.total
    
    # Update the first order with combined items
    order1.order = combined_order_items
    order1.total = combined_total
    
    # Release the second table
    table2.is_occupied = False
    table2.current_order_id = None
    table2.status = "available"
    # Ensure seats is not None before iterating
    if table2.seats is None:
        table2.seats = []
    for seat in table2.seats:
        seat["status"] = "available"
        seat["customer_name"] = None
    
    # Update the first table to reflect that it now contains both tables' customers
    table1.capacity = table1.capacity + table2.capacity
    # Ensure seats is not None before working with it
    if table1.seats is None:
        table1.seats = []
    # Extend seats array
    for i in range(len(table1.seats), table1.capacity):
        table1.seats.append({"seat_number": i+1, "status": "occupied", "customer_name": None})
    
    return table1

@router.post("/split-bill/{table_id}", response_model=List[OrderResponse])
def split_bill(table_id: int, split_details: dict):
    """Split a bill at a table into separate orders"""
    table = next((t for t in sample_tables if t.id == table_id), None)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    if not table.is_occupied:
        raise HTTPException(status_code=400, detail="Table must be occupied to split bill")
    
    # Get the current order
    current_order = next((o for o in sample_orders if o.id == table.current_order_id), None)
    if not current_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Split details should contain how to divide the order
    # For example: {"split_1": [item_indices], "split_2": [item_indices]}
    new_orders = []
    
    # Create new orders based on split details
    for split_key, item_indices in split_details.items():
        # Create a new order with selected items
        split_items = [current_order.order[i] for i in item_indices]
        split_total = sum(item.price for item in split_items)
        
        new_order_id = len(sample_orders) + 1
        new_order = OrderResponse(
            id=new_order_id,
            order=split_items,
            total=split_total,
            table_id=table_id,  # Same table
            customer_count=len(item_indices),  # Approximate
            special_requests=None,
            timestamp=datetime.now()
        )
        sample_orders.append(new_order)
        new_orders.append(new_order)
    
    return new_orders

# Get occupied tables
@router.get("/occupied/", response_model=List[TableResponse])
def get_occupied_tables():
    """Get all occupied tables"""
    occupied_tables = [t for t in sample_tables if t.is_occupied]
    return occupied_tables

# Get available tables
@router.get("/available/", response_model=List[TableResponse])
def get_available_tables():
    """Get all available tables"""
    available_tables = [t for t in sample_tables if not t.is_occupied and t.status == "available"]
    return available_tables