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
    from app.schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse, KitchenOrderDetail, OrderItem
    from app.services.kot_service_simple import kot_service
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.kitchen import KitchenOrder
    from models.order import Order
    from schemas import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse, KitchenOrderDetail, OrderItem
    from services.kot_service_simple import kot_service

router = APIRouter(prefix="/api/kitchen", tags=["Kitchen"])

# Helper function to convert database models to response models
def kitchen_order_to_detail(kitchen_order: KitchenOrder, db_order: Order) -> KitchenOrderDetail:
    """Convert database KitchenOrder and Order models to KitchenOrderDetail response model"""
    # Parse order_data from JSON string
    try:
        order_items_data = json.loads(db_order.order_data) if db_order.order_data else []
    except (json.JSONDecodeError, TypeError):
        order_items_data = []
    
    # Convert order items to OrderItem objects
    order_item_objects = []
    for item in order_items_data:
        order_item_objects.append(
            OrderItem(
                name=item.get("name", ""),
                price=float(item.get("price", 0.0)),
                category=item.get("category", ""),
                modifiers=item.get("modifiers", [])
            )
        )
    
    # Properly handle order_type - don't default to "dine_in" if it's None
    order_type = db_order.order_type
    if order_type is None:
        order_type = "dine_in"  # Default to dine_in only if explicitly None
    
    # Convert table_number to string if it's an integer
    table_number = db_order.table_number
    if table_number is not None:
        table_number = str(table_number)
    
    return KitchenOrderDetail(
        id=kitchen_order.id,
        order_id=kitchen_order.order_id,
        status=kitchen_order.status,
        created_at=kitchen_order.created_at,
        updated_at=kitchen_order.updated_at,
        order_items=order_item_objects,
        total=float(db_order.total) if db_order.total is not None else 0.0,
        order_type=str(order_type) if order_type is not None else None,
        table_number=table_number,
        customer_name=db_order.customer_name
    )

@router.get("/orders", response_model=List[KitchenOrderDetail])
def get_kitchen_orders(db: Session = Depends(get_db)):
    """Get all orders for the kitchen display from database"""
    # Get all kitchen orders from database
    kitchen_orders = db.query(KitchenOrder).all()
    
    # Convert to response format with order details
    result = []
    for kitchen_order in kitchen_orders:
        # Find the corresponding order
        db_order = db.query(Order).filter(Order.id == kitchen_order.order_id).first()
        if db_order:
            result.append(kitchen_order_to_detail(kitchen_order, db_order))
    
    return result

@router.post("/orders", response_model=KitchenOrderResponse)
def create_kitchen_order(kitchen_order: KitchenOrderCreate, db: Session = Depends(get_db)):
    """Add a new order to the kitchen display in database"""
    # Check if kitchen order already exists
    existing_kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == kitchen_order.order_id).first()
    if existing_kitchen_order:
        return KitchenOrderResponse.from_orm(existing_kitchen_order)
    
    # Create new kitchen order in database
    db_kitchen_order = KitchenOrder(
        order_id=kitchen_order.order_id,
        status=kitchen_order.status
    )
    
    db.add(db_kitchen_order)
    db.commit()
    db.refresh(db_kitchen_order)
    
    return KitchenOrderResponse.from_orm(db_kitchen_order)

@router.post("/orders/{order_id}/print-kot")
def print_kitchen_order_ticket(order_id: int):
    """Generate and print Kitchen Order Ticket for a specific order"""
    try:
        results = kot_service.print_kot_for_order(order_id)
        # Check if any station failed
        failed_stations = [station for station, result in results.items() if not result.get("success", False)]
        
        if failed_stations:
            return {
                "message": f"Kitchen Order Ticket printed with issues. Failed stations: {', '.join(failed_stations)}",
                "results": results,
                "status": "partial_success"
            }
        else:
            return {
                "message": "Kitchen Order Ticket printed successfully",
                "results": results,
                "status": "success"
            }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error printing KOT: {str(e)}")

@router.put("/orders/{order_id}", response_model=KitchenOrderResponse)
def update_kitchen_order_status(order_id: int, kitchen_order_update: KitchenOrderUpdate, db: Session = Depends(get_db)):
    """Update the status of an order in the kitchen"""
    # Find the kitchen order
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    
    # Validate status - only allow valid statuses
    valid_statuses = ["pending", "preparing", "ready", "served"]
    if kitchen_order_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}")
    
    # Update the status
    kitchen_order.status = kitchen_order_update.status
    kitchen_order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(kitchen_order)
    
    return KitchenOrderResponse.from_orm(kitchen_order)

@router.delete("/orders/{order_id}")
def remove_kitchen_order(order_id: int, db: Session = Depends(get_db)):
    """Remove an order from the kitchen display (when it's completed)"""
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if kitchen_order:
        db.delete(kitchen_order)
        db.commit()
    
    return {"message": "Order removed from kitchen display"}

@router.post("/orders/{order_id}/mark-served")
def mark_order_as_served(order_id: int, db: Session = Depends(get_db)):
    """Mark an order as served and remove it from the kitchen display"""
    # Find the kitchen order
    kitchen_order = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
    if not kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    
    # Update the status to served
    kitchen_order.status = "served"
    kitchen_order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(kitchen_order)
    
    return {"message": "Order marked as served", "order_id": order_id, "status": "served"}

@router.get("/printers")
def get_kitchen_printers():
    """Get information about available kitchen printers and KDS systems"""
    return {
        "message": "Available kitchen printers and KDS systems",
        "printers": kot_service.printers
    }

@router.get("/printers/{printer_id}/status")
def get_printer_status(printer_id: str):
    """Get the status of a specific printer or KDS"""
    try:
        status = kot_service.get_printer_status(printer_id)
        if not status.get("success", False):
            raise HTTPException(status_code=404, detail=status.get("message", "Printer not found"))
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting printer status: {str(e)}")

@router.post("/printers/{printer_id}/test")
def test_kitchen_printer(printer_id: str):
    """Test connection to a specific kitchen printer or KDS"""
    try:
        if printer_id not in kot_service.printers:
            raise HTTPException(status_code=404, detail=f"Printer {printer_id} not found")
        
        # Create a simple test order for testing
        test_items = [
            OrderItem(
                name='Test Item',
                price=5.99,
                category='Test',
                modifiers=[]
            )
        ]
        
        test_order = KitchenOrderDetail(
            id=0,
            order_id=0,
            status='test',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            order_items=test_items,
            total=5.99,
            order_type='test',
            table_number='TEST',
            customer_name='Printer Test'
        )
        
        result = kot_service.send_to_printer(test_order, printer_id)
        return {
            "message": f"Test print sent to {printer_id}",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing printer: {str(e)}")