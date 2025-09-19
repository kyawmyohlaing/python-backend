from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.order import Order
    from app.models.menu import MenuItem
    from app.models.kitchen import KitchenOrder
    from app.models.table import Table
    from app.data.shared_data import sample_tables
    from app.services.kot_service_simple import kot_service
    from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse, OrderItem
    from app.schemas.kitchen_schema import KitchenOrderCreate, KitchenOrderResponse
    from app.schemas.table_schema import TableResponse
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.order import Order
    from models.menu import MenuItem
    from models.kitchen import KitchenOrder
    from models.table import Table
    from data.shared_data import sample_tables
    from services.kot_service_simple import kot_service
    from schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse, OrderItem
    from schemas.kitchen_schema import KitchenOrderCreate, KitchenOrderResponse
    from schemas.table_schema import TableResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"])

# Helper function to convert Order model to OrderResponse
def order_model_to_response(order: Order) -> OrderResponse:
    """Convert Order database model to OrderResponse Pydantic model"""
    # Parse order_data and modifiers from JSON strings
    order_items = json.loads(order.order_data) if order.order_data else []
    modifiers = json.loads(order.modifiers) if order.modifiers else None
    assigned_seats = json.loads(order.assigned_seats) if order.assigned_seats else None
    
    # Convert order items to OrderItem objects
    order_item_objects = [
        OrderItem(
            name=item.get("name", ""),
            price=item.get("price", 0.0),
            category=item.get("category", ""),
            modifiers=item.get("modifiers", [])
        ) for item in order_items
    ]
    
    return OrderResponse(
        id=order.id,
        order=order_item_objects,
        total=order.total,
        timestamp=order.created_at,
        table_id=order.table_id,
        customer_count=order.customer_count,
        special_requests=order.special_requests,
        assigned_seats=assigned_seats,
        order_type=order.order_type,
        table_number=order.table_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        modifiers=modifiers
    )

@router.get("/", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """Get all orders from database"""
    orders = db.query(Order).all()
    return [order_model_to_response(order) for order in orders]

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order by ID from database"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_model_to_response(order)

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order in database"""
    try:
        # Convert order items to JSON-serializable format
        order_items_dict = [
            {
                "name": item.name,
                "price": item.price,
                "category": item.category,
                "modifiers": item.modifiers or []
            }
            for item in order.order
        ]
        
        # Create new order in database
        db_order = Order(
            total=order.total,
            order_data=json.dumps(order_items_dict),
            table_id=order.table_id,
            customer_count=order.customer_count,
            special_requests=order.special_requests,
            assigned_seats=json.dumps(order.assigned_seats) if order.assigned_seats else None,
            order_type=order.order_type,
            table_number=order.table_number,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            delivery_address=order.delivery_address,
            modifiers=json.dumps(order.modifiers) if order.modifiers else None
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        # If this is a dine-in order with a table number, automatically assign the table
        if db_order.order_type == "dine_in" and db_order.table_number:
            # Look up the table by table number
            table = db.query(Table).filter(Table.table_number == int(db_order.table_number)).first()
            if table:
                # Assign the table to the order
                table.is_occupied = True
                table.current_order_id = db_order.id
                table.status = "occupied"
                
                # Mark all seats as occupied and assign customer name from order
                customer_name = getattr(db_order, 'customer_name', None)
                if table.seats:
                    for seat in table.seats:
                        seat["status"] = "occupied"
                        seat["customer_name"] = customer_name
                
                # Update the order's table_id to reference the actual table
                db_order.table_id = table.id
                
                db.commit()
                db.refresh(table)
                db.refresh(db_order)
        
        # Convert to response format
        response_order = order_model_to_response(db_order)
        
        # Only automatically add dine-in orders to the kitchen
        # Takeaway and delivery orders should not go to the kitchen
        if db_order.order_type == "dine_in":
            # Automatically add the order to the kitchen (using database now)
            kitchen_order = KitchenOrder(
                order_id=db_order.id,
                status="pending"
            )
            db.add(kitchen_order)
            db.commit()
            db.refresh(kitchen_order)
            
            # Automatically print KOT for the new order
            try:
                kot_service.print_kot_for_order(db_order.id)
            except Exception as e:
                # Log the error but don't fail the order creation
                print(f"Warning: Failed to print KOT for order {db_order.id}: {str(e)}")
        else:
            # For takeaway and delivery orders, we might want to handle them differently
            # For now, we'll just log that they were created
            print(f"Order {db_order.id} ({db_order.order_type}) created - not sent to kitchen")
        
        return response_order
    except Exception as e:
        # Log the error and rollback the transaction
        print(f"Error creating order: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """Update an existing order in database"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order fields if provided
    if order_update.order is not None:
        order_items_dict = [
            {
                "name": item.name,
                "price": item.price,
                "category": item.category,
                "modifiers": item.modifiers or []
            }
            for item in order_update.order
        ]
        db_order.order_data = json.dumps(order_items_dict)
    
    if order_update.total is not None:
        db_order.total = order_update.total
    
    if order_update.table_id is not None:
        # If table is being changed, update both old and new table statuses
        if db_order.table_id and db_order.table_id != order_update.table_id:
            # Release old table
            old_table = db.query(Table).filter(Table.id == db_order.table_id).first()
            if old_table:
                old_table.is_occupied = False
                old_table.current_order_id = None
                old_table.status = "available"
                # Release all seats
                for i, seat in enumerate(old_table.seats):
                    old_table.seats[i]["status"] = "available"
                    old_table.seats[i]["customer_name"] = None
        
        # Assign new table
        new_table = db.query(Table).filter(Table.id == order_update.table_id).first()
        if new_table:
            new_table.is_occupied = True
            new_table.current_order_id = order_id
            new_table.status = "occupied"
            
            # Assign seats if provided
            if order_update.assigned_seats:
                for seat_num in order_update.assigned_seats:
                    if seat_num <= len(new_table.seats):
                        new_table.seats[seat_num-1]["status"] = "occupied"
        
        db_order.table_id = order_update.table_id
    
    if order_update.customer_count is not None:
        db_order.customer_count = order_update.customer_count
    
    if order_update.special_requests is not None:
        db_order.special_requests = order_update.special_requests
    
    if order_update.assigned_seats is not None:
        db_order.assigned_seats = json.dumps(order_update.assigned_seats)
    
    # Update new order type fields if provided
    if order_update.order_type is not None:
        db_order.order_type = order_update.order_type
    
    if order_update.table_number is not None:
        db_order.table_number = order_update.table_number
    
    if order_update.customer_name is not None:
        db_order.customer_name = order_update.customer_name
    
    if order_update.customer_phone is not None:
        db_order.customer_phone = order_update.customer_phone
    
    if order_update.delivery_address is not None:
        db_order.delivery_address = order_update.delivery_address
    
    if order_update.modifiers is not None:
        db_order.modifiers = json.dumps(order_update.modifiers)
    
    db.commit()
    db.refresh(db_order)
    
    return order_model_to_response(db_order)

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: dict, db: Session = Depends(get_db)):
    """Update the status of an order"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Convert to response format for table management
    response_order = order_model_to_response(db_order)
    
    # Find the corresponding kitchen order (now using database)
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if kitchen_order:
        # Validate status - only allow valid statuses
        valid_statuses = ["pending", "preparing", "ready", "served"]
        new_status = status_update.get("status")
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
        
        # Update the kitchen order status
        kitchen_order.status = new_status
        kitchen_order.updated_at = datetime.now()
        
        # If the order is marked as served, we might want to release the table
        if new_status == "served" and response_order.order_type == "dine_in":
            # Release the table
            if response_order.table_id:
                table = db.query(Table).filter(Table.id == response_order.table_id).first()
                if table:
                    table.is_occupied = False
                    table.current_order_id = None
                    table.status = "available"
                    # Release all seats
                    for i, seat in enumerate(table.seats):
                        table.seats[i]["status"] = "available"
                        table.seats[i]["customer_name"] = None
    
    db.commit()
    if kitchen_order:
        db.refresh(kitchen_order)
    
    return order_model_to_response(db_order)

@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order from database"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Convert to response format for table management
    response_order = order_model_to_response(db_order)
    
    # If order has an assigned table, release it
    if response_order.table_id:
        table = db.query(Table).filter(Table.id == response_order.table_id).first()
        if table:
            table.is_occupied = False
            table.current_order_id = None
            table.status = "available"
            # Release all seats
            for i, seat in enumerate(table.seats):
                table.seats[i]["status"] = "available"
                table.seats[i]["customer_name"] = None
    
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}

@router.post("/{order_id}/mark-served")
def mark_order_as_served(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as served and release associated resources"""
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Convert to response format for table management
    response_order = order_model_to_response(db_order)
    
    # Find the corresponding kitchen order (now using database)
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if kitchen_order:
        # Update the kitchen order status to served
        kitchen_order.status = "served"
        kitchen_order.updated_at = datetime.now()
    
    # If it's a dine_in order, release the table
    if response_order.order_type == "dine_in":
        if response_order.table_id:
            table = db.query(Table).filter(Table.id == response_order.table_id).first()
            if table:
                table.is_occupied = False
                table.current_order_id = None
                table.status = "available"
                # Release all seats
                for i, seat in enumerate(table.seats):
                    table.seats[i]["status"] = "available"
                    table.seats[i]["customer_name"] = None
    
    db.commit()
    if kitchen_order:
        db.refresh(kitchen_order)
    
    return {"message": "Order marked as served", "order_id": order_id}