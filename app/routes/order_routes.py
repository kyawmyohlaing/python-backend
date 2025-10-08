from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.order import Order, OrderStatus, OrderType
    from app.models.order_item import OrderItem as OrderItemModel
    from app.models.table import Table
    from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse, OrderItem
    from app.models.user import User
    from app.schemas.user_schema import UserResponse
    from app.dependencies import get_current_user
    from app.models.kitchen import KitchenOrder
    from app.schemas.kitchen_schema import KitchenOrderCreate, KitchenOrderResponse
    from app.schemas.table_schema import TableResponse
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.order import Order, OrderStatus, OrderType
    from models.order_item import OrderItem as OrderItemModel
    from models.table import Table
    from schemas.order_schema import OrderCreate, OrderUpdate, OrderResponse, OrderItem
    from models.user import User
    from schemas.user_schema import UserResponse
    from dependencies import get_current_user
    from models.kitchen import KitchenOrder
    from schemas.kitchen_schema import KitchenOrderCreate, KitchenOrderResponse
    from schemas.table_schema import TableResponse

router = APIRouter(prefix="/api/orders", tags=["Orders"])

# Helper function to convert Order model to OrderResponse
def order_model_to_response(order: Order) -> OrderResponse:
    """Convert Order database model to OrderResponse Pydantic model"""
    # Parse order_data and modifiers from JSON strings
    try:
        order_items = json.loads(order.order_data) if order.order_data else []
    except (json.JSONDecodeError, TypeError):
        order_items = []
    
    try:
        modifiers = json.loads(order.modifiers) if order.modifiers else None
    except (json.JSONDecodeError, TypeError):
        modifiers = None
        
    try:
        assigned_seats = json.loads(order.assigned_seats) if order.assigned_seats else None
    except (json.JSONDecodeError, TypeError):
        assigned_seats = None
    
    # Convert order items to OrderItem objects
    order_item_objects = [
        OrderItem(
            name=item.get("name", ""),
            price=item.get("price", 0.0),
            category=item.get("category", ""),
            modifiers=item.get("modifiers", [])
        ) for item in order_items
    ]
    
    # Handle order_type properly
    order_type_value = None
    if order.order_type is not None:
        order_type_value = order.order_type.value if hasattr(order.order_type, 'value') else str(order.order_type)
    
    # Handle payment_type properly
    payment_type_value = None
    if order.payment_type is not None:
        payment_type_value = order.payment_type.value if hasattr(order.payment_type, 'value') else str(order.payment_type)
    else:
        payment_type_value = "cash"
    
    return OrderResponse(
        id=order.id,
        order=order_item_objects,
        total=order.total or 0.0,
        table_id=order.table_id,
        customer_count=order.customer_count,
        special_requests=order.special_requests,
        timestamp=order.created_at or datetime.utcnow(),
        order_type=order_type_value,
        table_number=str(order.table_number) if order.table_number is not None else None,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        assigned_seats=assigned_seats,
        modifiers=modifiers,
        payment_type=payment_type_value
    )

@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new order.
    """
    # Convert order items to JSON string
    order_data_json = json.dumps([item.dict() for item in order.order])
    
    # Convert modifiers to JSON string if provided
    modifiers_json = json.dumps(order.modifiers) if order.modifiers else None
    
    # Convert assigned_seats to JSON string if provided
    assigned_seats_json = json.dumps(order.assigned_seats) if order.assigned_seats else None
    
    # Convert payment_type to enum if provided
    payment_type = order.payment_type
    if payment_type:
        # Validate payment type
        valid_payment_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
        if payment_type not in valid_payment_types:
            payment_type = "cash"  # Default to cash if invalid
    
    # If table_number is provided, look up the corresponding table and set table_id
    table_id = order.table_id
    table = None
    if order.table_number and not table_id:
        # Look up table by table_number
        table = db.query(Table).filter(Table.table_number == order.table_number).first()
        if table:
            table_id = table.id
    
    # Create new order
    db_order = Order(
        total=order.total,
        order_data=order_data_json,
        table_id=table_id,  # Use the looked up table_id if available
        customer_count=order.customer_count,
        special_requests=order.special_requests,
        created_by=current_user.id,
        order_type=order.order_type,
        table_number=order.table_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        modifiers=modifiers_json,
        assigned_seats=assigned_seats_json,
        payment_type=payment_type
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Automatically create a kitchen order for this order
    try:
        from app.models.kitchen import KitchenOrder
        kitchen_order = KitchenOrder(
            order_id=db_order.id,
            status="pending"
        )
        db.add(kitchen_order)
        db.commit()
        db.refresh(kitchen_order)
    except Exception as e:
        # If kitchen order creation fails, log the error but don't fail the order creation
        print(f"Warning: Failed to create kitchen order for order {db_order.id}: {str(e)}")
        db.rollback()  # Rollback just the kitchen order creation
    
    # If this is a dine-in order with a table, automatically assign the table to this order
    if (order.order_type == OrderType.DINE_IN or 
        (isinstance(order.order_type, str) and order.order_type.lower() == 'dine_in')) and table:
        try:
            # Update table status to occupied
            table.is_occupied = True
            table.current_order_id = db_order.id
            table.status = "occupied"
            
            # Mark all seats as occupied
            if table.seats:
                for seat in table.seats:
                    seat["status"] = "occupied"
                    # Get customer name from order if available
                    if db_order.customer_name:
                        seat["customer_name"] = db_order.customer_name
            
            db.commit()
            db.refresh(table)
        except Exception as e:
            # If table assignment fails, log the error but don't fail the order creation
            print(f"Warning: Failed to automatically assign table {table.id} to order {db_order.id}: {str(e)}")
    
    return order_model_to_response(db_order)

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all orders.
    """
    orders = db.query(Order).offset(skip).limit(limit).all()
    return [order_model_to_response(order) for order in orders]

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific order by ID.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_model_to_response(order)

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing order.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order fields if provided
    update_data = order_update.dict(exclude_unset=True)
    
    # Handle special fields that need JSON conversion
    if "order" in update_data and update_data["order"] is not None:
        db_order.order_data = json.dumps([item.dict() for item in update_data["order"]])
        # Remove from update_data to avoid double processing
        del update_data["order"]
    
    if "modifiers" in update_data and update_data["modifiers"] is not None:
        db_order.modifiers = json.dumps(update_data["modifiers"])
        del update_data["modifiers"]
        
    if "assigned_seats" in update_data and update_data["assigned_seats"] is not None:
        db_order.assigned_seats = json.dumps(update_data["assigned_seats"])
        del update_data["assigned_seats"]
    
    # Handle payment_type validation
    if "payment_type" in update_data and update_data["payment_type"] is not None:
        payment_type = update_data["payment_type"]
        # Validate payment type
        valid_payment_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
        if payment_type in valid_payment_types:
            db_order.payment_type = payment_type
        del update_data["payment_type"]
    
    # Update remaining fields
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    
    return order_model_to_response(db_order)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an order.
    """
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return