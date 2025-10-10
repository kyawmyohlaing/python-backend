from fastapi import APIRouter, HTTPException, Depends, Form
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from typing import List
from datetime import datetime
import json

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.table import Table
    from app.models.order import Order
    from app.schemas.order_schema import OrderResponse, OrderItem
    from app.schemas.table_schema import TableResponse, TableCreate, TableUpdate
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.table import Table
    from models.order import Order
    from schemas.order_schema import OrderResponse, OrderItem
    from schemas.table_schema import TableResponse, TableCreate, TableUpdate

router = APIRouter(prefix="/api/tables", tags=["Tables"])

@router.get("/", response_model=List[TableResponse])
def get_tables(db: Session = Depends(get_db)):
    """Get all tables from database"""
    tables = db.query(Table).all()
    return [TableResponse.model_validate(table) for table in tables]

@router.get("/{table_id}", response_model=TableResponse)
def get_table(table_id: int, db: Session = Depends(get_db)):
    """Get a specific table by ID from database"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return TableResponse.model_validate(table)

@router.post("/", response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """Create a new table in database"""
    # Check if table number already exists
    existing_table = db.query(Table).filter(Table.table_number == table.table_number).first()
    if existing_table:
        raise HTTPException(status_code=400, detail="Table number already exists")
    
    # Initialize seats array with default values
    seats = [{"seat_number": i+1, "status": "available", "customer_name": None} for i in range(table.capacity)]
    
    db_table = Table(
        table_number=table.table_number,
        capacity=table.capacity,
        is_occupied=False,
        current_order_id=None,
        status="available",
        seats=seats
    )
    
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    
    return TableResponse.model_validate(db_table)

@router.put("/{table_id}", response_model=TableResponse)
def update_table(table_id: int, table_update: TableUpdate, db: Session = Depends(get_db)):
    """Update a table"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Update table fields if provided
    if table_update.table_number is not None:
        # Check if new table number already exists (and it's not the current table)
        existing_table = db.query(Table).filter(Table.table_number == table_update.table_number, Table.id != table_id).first()
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
    
    db.commit()
    db.refresh(table)
    return TableResponse.model_validate(table)

@router.delete("/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """Delete a table"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if table is occupied
    if table.is_occupied:
        raise HTTPException(status_code=400, detail="Cannot delete an occupied table")
    
    db.delete(table)
    db.commit()
    return {"message": "Table deleted successfully"}

# Table assignment functions
@router.post("/{table_id}/assign/{order_id}", response_model=TableResponse)
def assign_table_to_order(table_id: int, order_id: int, db: Session = Depends(get_db)):
    """Assign a table to an order"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    # Check if order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if table is already occupied
    if table.is_occupied:
        raise HTTPException(status_code=400, detail="Table is already occupied")
    
    # Update table status
    table.is_occupied = True
    table.current_order_id = order_id
    table.status = "occupied"
    
    # Mark all seats as occupied and assign customer name from order
    # Ensure seats is not None before iterating
    if table.seats is None:
        table.seats = []
    
    # Get customer name from order if available
    customer_name = getattr(order, 'customer_name', None)
    
    for seat in table.seats:
        seat["status"] = "occupied"
        seat["customer_name"] = customer_name
    
    db.commit()
    db.refresh(table)
    return TableResponse.model_validate(table)

@router.post("/{table_id}/release", response_model=TableResponse)
def release_table(table_id: int, db: Session = Depends(get_db)):
    """Release a table (mark as available)"""
    table = db.query(Table).filter(Table.id == table_id).first()
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
    
    db.commit()
    db.refresh(table)
    return TableResponse.model_validate(table)

# Seat management functions
@router.post("/{table_id}/assign-seat/{seat_number}")
def assign_seat(
    table_id: int, 
    seat_number: int, 
    customer_name: str = Form(default=""), 
    db: Session = Depends(get_db)
):
    """Assign a specific seat at a table"""
    table = db.query(Table).filter(Table.id == table_id).first()
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

    # IMPORTANT: Update the table's seats field in the database
    # In SQLAlchemy, JSON fields need to be explicitly marked as modified
    flag_modified(table, 'seats')

    db.commit()
    db.refresh(table)
    return {"message": f"Seat {seat_number} assigned successfully"}

@router.post("/{table_id}/release-seat/{seat_number}")
def release_seat(
    table_id: int, 
    seat_number: int, 
    db: Session = Depends(get_db)
):
    """Release a specific seat at a table"""
    table = db.query(Table).filter(Table.id == table_id).first()
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

    # IMPORTANT: Update the table's seats field in the database
    # In SQLAlchemy, JSON fields need to be explicitly marked as modified
    flag_modified(table, 'seats')

    db.commit()
    db.refresh(table)
    return {"message": f"Seat {seat_number} released successfully"}

# Merge/Split bill functions
@router.post("/merge-tables/{table_id_1}/{table_id_2}", response_model=TableResponse)
def merge_tables(table_id_1: int, table_id_2: int, db: Session = Depends(get_db)):
    """Merge two tables into one order"""
    table1 = db.query(Table).filter(Table.id == table_id_1).first()
    table2 = db.query(Table).filter(Table.id == table_id_2).first()
    
    if not table1 or not table2:
        raise HTTPException(status_code=404, detail="One or both tables not found")
    
    if not table1.is_occupied or not table2.is_occupied:
        raise HTTPException(status_code=400, detail="Both tables must be occupied to merge")
    
    # Get the orders for both tables
    order1 = db.query(Order).filter(Order.id == table1.current_order_id).first()
    order2 = db.query(Order).filter(Order.id == table2.current_order_id).first()
    
    if not order1 or not order2:
        raise HTTPException(status_code=404, detail="Orders not found for one or both tables")
    
    # Combine orders (in a real app, you might want to create a new order)
    # For simplicity, we'll merge into the first order
    # Parse order_data from JSON strings
    order1_items = json.loads(order1.order_data) if order1.order_data else []
    order2_items = json.loads(order2.order_data) if order2.order_data else []
    
    combined_order_items = order1_items + order2_items
    combined_total = order1.total + order2.total
    
    # Update the first order with combined items
    order1.order_data = json.dumps(combined_order_items)
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
    
    db.commit()
    db.refresh(table1)
    db.refresh(table2)
    return TableResponse.model_validate(table1)

@router.post("/{table_id}/split-bill", response_model=List[OrderResponse])
def split_bill(table_id: int, split_request: dict, db: Session = Depends(get_db)):
    """Split a bill at a table into separate orders by seat or item"""
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    
    if not table.is_occupied:
        raise HTTPException(status_code=400, detail="Table must be occupied to split bill")
    
    # Get the current order
    current_order = db.query(Order).filter(Order.id == table.current_order_id).first()
    if not current_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Parse order_data from JSON string
    current_order_items = json.loads(current_order.order_data) if current_order.order_data else []
    
    # Split details should contain how to divide the order
    # For example: {"method": "items", "splits": [{"items": [0, 1]}, {"items": [2, 3]}]}
    # or: {"method": "seats", "seat_assignments": {"1": [0, 1], "2": [2, 3]}}
    
    method = split_request.get("method", "items")
    new_orders = []
    
    if method == "items":
        # Split by specific items
        splits = split_request.get("splits", [])
        for split in splits:
            item_indices = split.get("items", [])
            # Create a new order with selected items
            split_items = [current_order_items[i] for i in item_indices if i < len(current_order_items)]
            split_total = sum(item.get("price", 0.0) for item in split_items)
            
            # Convert items to OrderItem objects for response
            order_item_objects = [
                OrderItem(
                    name=item.get("name", ""),
                    price=item.get("price", 0.0),
                    category=item.get("category", ""),
                    modifiers=item.get("modifiers", [])
                ) for item in split_items
            ]
            
            # Create new order in database
            new_order = Order(
                total=split_total,
                order_data=json.dumps(split_items),
                table_id=table_id,
                customer_count=len(item_indices),
                special_requests=current_order.special_requests,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                order_type=current_order.order_type,
                table_number=str(current_order.table_number) if current_order.table_number is not None else None,
                customer_name=current_order.customer_name,
                created_by=current_order.created_by
            )
            
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            
            # Convert to response format
            new_order_response = OrderResponse(
                id=new_order.id,
                order=order_item_objects,
                total=new_order.total,
                table_id=new_order.table_id,
                customer_count=new_order.customer_count,
                special_requests=new_order.special_requests,
                timestamp=new_order.created_at,
                order_type=new_order.order_type,
                table_number=str(new_order.table_number) if new_order.table_number is not None else None,
                customer_name=new_order.customer_name
            )
            
            new_orders.append(new_order_response)
    
    elif method == "seats":
        # Split by seats
        seat_assignments = split_request.get("seat_assignments", {})
        for seat_number, item_indices in seat_assignments.items():
            # Create a new order with selected items
            split_items = [current_order_items[i] for i in item_indices if i < len(current_order_items)]
            split_total = sum(item.get("price", 0.0) for item in split_items)
            
            # Convert items to OrderItem objects for response
            order_item_objects = [
                OrderItem(
                    name=item.get("name", ""),
                    price=item.get("price", 0.0),
                    category=item.get("category", ""),
                    modifiers=item.get("modifiers", [])
                ) for item in split_items
            ]
            
            # Create new order in database
            new_order = Order(
                total=split_total,
                order_data=json.dumps(split_items),
                table_id=table_id,
                customer_count=1,
                special_requests=current_order.special_requests,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                order_type=current_order.order_type,
                table_number=str(current_order.table_number) if current_order.table_number is not None else None,
                customer_name=f"Seat {seat_number}",
                created_by=current_order.created_by
            )
            
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            
            # Convert to response format
            new_order_response = OrderResponse(
                id=new_order.id,
                order=order_item_objects,
                total=new_order.total,
                table_id=new_order.table_id,
                customer_count=new_order.customer_count,
                special_requests=new_order.special_requests,
                timestamp=new_order.created_at,
                order_type=new_order.order_type,
                table_number=str(new_order.table_number) if new_order.table_number is not None else None,
                customer_name=new_order.customer_name
            )
            
            new_orders.append(new_order_response)
    
    elif method == "equal":
        # Split equally among specified number of parts
        parts = split_request.get("parts", 2)
        if parts <= 0:
            raise HTTPException(status_code=400, detail="Parts must be greater than 0")
        
        # Distribute items as evenly as possible
        for i in range(parts):
            # Calculate which items go to this part
            part_items = current_order_items[i::parts]
            split_total = sum(item.get("price", 0.0) for item in part_items)
            
            # Convert items to OrderItem objects for response
            order_item_objects = [
                OrderItem(
                    name=item.get("name", ""),
                    price=item.get("price", 0.0),
                    category=item.get("category", ""),
                    modifiers=item.get("modifiers", [])
                ) for item in part_items
            ]
            
            # Create new order in database
            new_order = Order(
                total=split_total,
                order_data=json.dumps(part_items),
                table_id=table_id,
                customer_count=len(part_items),
                special_requests=current_order.special_requests,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                order_type=current_order.order_type,
                table_number=str(current_order.table_number) if current_order.table_number is not None else None,
                customer_name=f"Part {i+1}",
                created_by=current_order.created_by
            )
            
            db.add(new_order)
            db.commit()
            db.refresh(new_order)
            
            # Convert to response format
            new_order_response = OrderResponse(
                id=new_order.id,
                order=order_item_objects,
                total=new_order.total,
                table_id=new_order.table_id,
                customer_count=new_order.customer_count,
                special_requests=new_order.special_requests,
                timestamp=new_order.created_at,
                order_type=new_order.order_type,
                table_number=str(new_order.table_number) if new_order.table_number is not None else None,
                customer_name=new_order.customer_name
            )
            
            new_orders.append(new_order_response)
    
    else:
        raise HTTPException(status_code=400, detail="Invalid split method. Use 'items', 'seats', or 'equal'")
    
    return new_orders

# Get occupied tables
@router.get("/occupied/", response_model=List[TableResponse])
def get_occupied_tables(db: Session = Depends(get_db)):
    """Get all occupied tables"""
    occupied_tables = db.query(Table).filter(Table.is_occupied == True).all()
    return [TableResponse.model_validate(table) for table in occupied_tables]

# Get available tables
@router.get("/available/", response_model=List[TableResponse])
def get_available_tables(db: Session = Depends(get_db)):
    """Get all available tables"""
    available_tables = db.query(Table).filter(Table.is_occupied == False, Table.status == "available").all()
    return [TableResponse.model_validate(table) for table in available_tables]