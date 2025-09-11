from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from models.kitchen import KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse, KitchenOrderDetail
from models.order import OrderResponse
from data.shared_data import sample_orders, sample_kitchen_orders
from services.kot_service import kot_service

router = APIRouter(prefix="/api/kitchen", tags=["Kitchen"])

@router.get("/orders", response_model=List[KitchenOrderDetail])
def get_kitchen_orders():
    """Get all orders for the kitchen display"""
    # In a real application, this would join with the orders table
    # For now, we'll simulate the data
    kitchen_orders = []
    for kitchen_order in sample_kitchen_orders:
        # Find the corresponding order
        order = next((o for o in sample_orders if o.id == kitchen_order.order_id), None)
        if order:
            kitchen_orders.append(KitchenOrderDetail(
                id=kitchen_order.id,
                order_id=kitchen_order.order_id,
                status=kitchen_order.status,
                created_at=kitchen_order.created_at,
                updated_at=kitchen_order.updated_at,
                order_items=order.order,
                total=order.total,
                # Add order type information
                order_type=order.order_type,
                table_number=order.table_number,
                customer_name=order.customer_name
            ))
    return kitchen_orders

@router.post("/orders", response_model=KitchenOrderResponse)
def create_kitchen_order(kitchen_order: KitchenOrderCreate):
    """Add a new order to the kitchen display"""
    # In a real application, this would save to the database
    new_id = len(sample_kitchen_orders) + 1
    new_kitchen_order = KitchenOrderResponse(
        id=new_id,
        order_id=kitchen_order.order_id,
        status=kitchen_order.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    sample_kitchen_orders.append(new_kitchen_order)
    return new_kitchen_order

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
def update_kitchen_order_status(order_id: int, kitchen_order_update: KitchenOrderUpdate):
    """Update the status of an order in the kitchen"""
    # Find the kitchen order
    kitchen_order = next((ko for ko in sample_kitchen_orders if ko.order_id == order_id), None)
    if not kitchen_order:
        raise HTTPException(status_code=404, detail="Kitchen order not found")
    
    # Update the status
    kitchen_order.status = kitchen_order_update.status
    kitchen_order.updated_at = datetime.now()
    return kitchen_order

@router.delete("/orders/{order_id}")
def remove_kitchen_order(order_id: int):
    """Remove an order from the kitchen display (when it's completed)"""
    global sample_kitchen_orders
    sample_kitchen_orders = [ko for ko in sample_kitchen_orders if ko.order_id != order_id]
    return {"message": "Order removed from kitchen display"}

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
            type('MenuItem', (), {'name': 'Test Item', 'price': 5.99, 'category': 'Test'})()
        ]
        
        test_order = type('KitchenOrderDetail', (), {
            'id': 0,
            'order_id': 0,
            'status': 'test',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'order_items': test_items,
            'total': 5.99,
            'order_type': 'test',
            'table_number': 'TEST',
            'customer_name': 'Printer Test'
        })()
        
        result = kot_service.send_to_printer(test_order, printer_id)
        return {
            "message": f"Test print sent to {printer_id}",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing printer: {str(e)}")