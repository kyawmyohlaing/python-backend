from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.table import TableCreate, TableUpdate, TableResponse
from models.order import OrderResponse

router = APIRouter(prefix="/api/tables", tags=["Tables"])

# Sample tables data - in a real application, this would be stored in a database
sample_tables = [
    TableResponse(
        id=1,
        table_number=1,
        capacity=4,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=2,
        table_number=2,
        capacity=2,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=3,
        table_number=3,
        capacity=6,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=4,
        table_number=4,
        capacity=4,
        is_occupied=False,
        current_order_id=None,
        status="available"
    )
]

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
    
    new_id = len(sample_tables) + 1
    new_table = TableResponse(
        id=new_id,
        table_number=table.table_number,
        capacity=table.capacity,
        is_occupied=False,
        current_order_id=None,
        status="available"
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
    
    if table_update.is_occupied is not None:
        table.is_occupied = table_update.is_occupied
    
    if table_update.current_order_id is not None:
        table.current_order_id = table_update.current_order_id
    
    if table_update.status is not None:
        table.status = table_update.status
    
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
    
    # Check if table is already occupied
    if table.is_occupied:
        raise HTTPException(status_code=400, detail="Table is already occupied")
    
    # Update table status
    table.is_occupied = True
    table.current_order_id = order_id
    table.status = "occupied"
    
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
    
    return table

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