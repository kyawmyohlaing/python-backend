from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import json

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.kitchen import KitchenOrder
    from app.models.order import Order
    from app.schemas import BarOrderCreate, BarOrderUpdate, BarOrderResponse, BarOrderDetail, OrderItem
    from app.services.kot_service_simple import kot_service
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.kitchen import KitchenOrder
    from models.order import Order
    from schemas import BarOrderCreate, BarOrderUpdate, BarOrderResponse, BarOrderDetail, OrderItem
    from services.kot_service_simple import kot_service

router = APIRouter(prefix="/api/bar", tags=["Bar"])

# Helper function to convert database models to response models
def bar_order_to_detail(kitchen_order: KitchenOrder, db_order: Order) -> BarOrderDetail:
    """Convert database KitchenOrder and Order models to BarOrderDetail response model"""
    # Parse order_data from JSON string
    try:
        # Access column value properly to avoid type checking issues
        order_data_value = getattr(db_order, 'order_data', None)
        order_data_str = str(order_data_value) if order_data_value is not None else "[]"
        order_items_data = json.loads(order_data_str) if order_data_str else []
    except (json.JSONDecodeError, TypeError):
        order_items_data = []
    
    # Convert order items to OrderItem objects
    order_item_objects = []
    for item in order_items_data:
        order_item_objects.append(
            OrderItem(
                name=str(item.get("name", "")),
                price=float(item.get("price", 0.0)),
                category=str(item.get("category", "")),
                modifiers=item.get("modifiers", [])
            )
        )
    
    # Properly handle order_type - don't default to "dine_in" if it's None
    order_type_value = getattr(db_order, 'order_type', None)
    order_type = str(order_type_value) if order_type_value is not None else "dine_in"
    
    # Convert table_number to string if it's an integer
    table_number_value = getattr(db_order, 'table_number', None)
    table_number = str(table_number_value) if table_number_value is not None else None
    
    # Access column values properly using getattr
    kitchen_order_id = int(getattr(kitchen_order, 'id', 0))
    kitchen_order_order_id = int(getattr(kitchen_order, 'order_id', 0))
    kitchen_order_status = str(getattr(kitchen_order, 'status', 'pending'))
    kitchen_order_created_at = getattr(kitchen_order, 'created_at', datetime.utcnow())
    kitchen_order_updated_at = getattr(kitchen_order, 'updated_at', datetime.utcnow())
    
    # Get values from db_order using getattr
    db_order_total = float(getattr(db_order, 'total', 0.0)) if getattr(db_order, 'total', None) is not None else 0.0
    db_order_customer_name = str(getattr(db_order, 'customer_name', '')) if getattr(db_order, 'customer_name', None) is not None else None
    
    return BarOrderDetail(
        id=kitchen_order_id,
        order_id=kitchen_order_order_id,
        status=kitchen_order_status,
        created_at=kitchen_order_created_at,
        updated_at=kitchen_order_updated_at,
        order_items=order_item_objects,
        total=db_order_total,
        order_type=order_type,
        table_number=table_number,
        customer_name=db_order_customer_name
    )

# Helper function to determine if an item is a drink
def is_drink_item(item):
    """Determine if an item is a drink based on category or name"""
    drink_categories = ['drink', 'beverage', 'cocktail', 'wine', 'beer', 'alcohol', 'soft drink']
    drink_keywords = ['coffee', 'tea', 'soda', 'juice', 'smoothie', 'cocktail', 'wine', 'beer', 'alcohol']
    
    # Check category
    if item.get('category'):
        category = item.get('category', '').lower()
        if any(drink_cat in category for drink_cat in drink_categories):
            return True
    
    # Check name
    if item.get('name'):
        name = item.get('name', '').lower()
        # Use exact word matching to prevent substring matches
        for keyword in drink_keywords:
            # Special handling for food items that might contain drink keywords
            food_exceptions = ['coffee cake', 'tea sandwich', 'coffee ice cream', 'tea cookies', 'tea cake']
            if keyword in name and not any(exception in name for exception in food_exceptions):
                # Make sure it's a whole word match
                import re
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, name):
                    return True
    
    return False

@router.get("/orders", response_model=List[BarOrderDetail])
def get_bar_orders(db: Session = Depends(get_db)):
    """Get all orders for the bar display from database that contain drink items"""
    # Get all kitchen orders from database
    kitchen_orders = db.query(KitchenOrder).all()
    
    # Convert to response format with order details, filtering for drink items
    result = []
    for kitchen_order in kitchen_orders:
        # Find the corresponding order
        db_order = db.query(Order).filter(Order.id == kitchen_order.order_id).first()
        if db_order:
            # Parse order_data to check if it contains drink items
            try:
                # Access column value properly to avoid type checking issues
                order_data_value = getattr(db_order, 'order_data', None)
                order_data_str = str(order_data_value) if order_data_value is not None else "[]"
                order_items_data = json.loads(order_data_str) if order_data_str else []
            except (json.JSONDecodeError, TypeError):
                order_items_data = []
            
            # Check if any item in the order is a drink
            has_drink_items = any(is_drink_item(item) for item in order_items_data)
            
            if has_drink_items:
                result.append(bar_order_to_detail(kitchen_order, db_order))
    
    return result

@router.post("/orders", response_model=BarOrderResponse)
def create_bar_order(bar_order: BarOrderCreate, db: Session = Depends(get_db)):
    """Add a new order to the bar display in database"""
    # Check if kitchen order already exists
    existing_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == bar_order.order_id).first()
    if existing_kitchen_order:
        return BarOrderResponse.from_orm(existing_kitchen_order)
    
    # Create new kitchen order in database (Bar uses the same KitchenOrder model)
    db_kitchen_order = KitchenOrder(
        order_id=bar_order.order_id,
        status=bar_order.status
    )
    
    db.add(db_kitchen_order)
    db.commit()
    db.refresh(db_kitchen_order)
    
    return BarOrderResponse.from_orm(db_kitchen_order)

@router.post("/orders/{order_id}/print-bot")
def print_bar_order_ticket(order_id: int):
    """Generate and print Bar Order Ticket for a specific order"""
    try:
        results = kot_service.print_kot_for_order(order_id)
        # Check if any station failed
        failed_stations = [station for station, result in results.items() if not result.get("success", False)]
        
        if failed_stations:
            return {
                "message": f"Bar Order Ticket printed with issues. Failed stations: {', '.join(failed_stations)}",
                "results": results,
                "status": "partial_success"
            }
        else:
            return {
                "message": "Bar Order Ticket printed successfully",
                "results": results,
                "status": "success"
            }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error printing BOT: {str(e)}")

@router.put("/orders/{order_id}", response_model=BarOrderResponse)
def update_bar_order_status(order_id: int, bar_order_update: BarOrderUpdate, db: Session = Depends(get_db)):
    """Update the status of an order in the bar"""
    # Find the kitchen order (Bar uses the same KitchenOrder model)
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    
    # If kitchen order doesn't exist, create it
    if not kitchen_order:
        # Check if the order exists in the main orders table
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Create a new kitchen order with default status 'pending'
        kitchen_order = KitchenOrder(
            order_id=order_id,
            status="pending"
        )
        db.add(kitchen_order)
        db.commit()
        db.refresh(kitchen_order)
    
    # Validate status - only allow valid statuses
    valid_statuses = ["pending", "preparing", "ready", "served"]
    if bar_order_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    # Update the status (this works in kitchen routes, so it should work here too)
    kitchen_order.status = bar_order_update.status
    kitchen_order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(kitchen_order)
    
    # Return BarOrderResponse (convert from KitchenOrder)
    return BarOrderResponse.from_orm(kitchen_order)

@router.post("/orders/{order_id}/mark-served")
def mark_order_as_served(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as served and remove it from the bar display"""
    # Find the kitchen order
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not kitchen_order:
        raise HTTPException(status_code=404, detail="Bar order not found")
    
    # Update the status to served
    kitchen_order.status = "served"
    kitchen_order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(kitchen_order)
    
    return {"message": "Order marked as served", "order_id": order_id, "status": "served"}
