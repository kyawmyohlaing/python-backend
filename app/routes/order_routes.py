from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
from database import get_db
from models.order import Order, OrderCreate, OrderUpdate, OrderResponse, OrderItem
from models.menu import MenuItem
from models.kitchen import KitchenOrderCreate, KitchenOrderResponse
from models.table import TableResponse
from data.shared_data import sample_orders, sample_kitchen_orders, sample_tables
from services.kot_service import kot_service

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderResponse])
def get_orders():
    """Get all orders"""
    return sample_orders

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    """Get a specific order by ID"""
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    """Create a new order"""
    # In a real application, this would save to the database
    new_id = len(sample_orders) + 1
    
    # Create new order with all the fields from the request
    new_order = OrderResponse(
        id=new_id,
        order=order.order,
        total=order.total,
        table_id=order.table_id,
        customer_count=order.customer_count,
        special_requests=order.special_requests,
        assigned_seats=order.assigned_seats,
        # Include new order type fields
        order_type=order.order_type,
        table_number=order.table_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        delivery_address=order.delivery_address,
        modifiers=order.modifiers,
        timestamp=datetime.now()
    )
    sample_orders.append(new_order)
    
    # Automatically add the order to the kitchen
    kitchen_order = KitchenOrderResponse(
        id=len(sample_kitchen_orders) + 1,
        order_id=new_id,
        status="pending",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    sample_kitchen_orders.append(kitchen_order)
    
    # Automatically print KOT for the new order
    try:
        kot_service.print_kot_for_order(new_id)
    except Exception as e:
        # Log the error but don't fail the order creation
        print(f"Warning: Failed to print KOT for order {new_id}: {str(e)}")
    
    # Handle table assignment based on order type
    if new_order.order_type == "dine-in":
        # For dine-in orders, we need a table
        # First check if table_id is provided
        if new_order.table_id:
            table = next((t for t in sample_tables if t.id == new_order.table_id), None)
            if table:
                table.is_occupied = True
                table.current_order_id = new_id
                table.status = "occupied"
                
                # Assign seats if provided and table.seats is not None
                if new_order.assigned_seats and table.seats:
                    for seat_num in new_order.assigned_seats:
                        if seat_num <= len(table.seats):
                            table.seats[seat_num-1]["status"] = "occupied"
                            table.seats[seat_num-1]["customer_name"] = new_order.customer_name
        # If no table_id but table_number is provided, find table by number
        elif new_order.table_number:
            table = next((t for t in sample_tables if str(t.table_number) == str(new_order.table_number)), None)
            if table:
                table.is_occupied = True
                table.current_order_id = new_id
                table.status = "occupied"
                
                # Assign seats if provided and table.seats is not None
                if new_order.assigned_seats and table.seats:
                    for seat_num in new_order.assigned_seats:
                        if seat_num <= len(table.seats):
                            table.seats[seat_num-1]["status"] = "occupied"
                            table.seats[seat_num-1]["customer_name"] = new_order.customer_name
                # Also set the table_id on the order for consistency
                new_order.table_id = table.id
    
    return new_order

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order_update: OrderUpdate):
    """Update an existing order"""
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Update order fields if provided
    if order_update.order is not None:
        order.order = order_update.order
    
    if order_update.total is not None:
        order.total = order_update.total
    
    if order_update.table_id is not None:
        # If table is being changed, update both old and new table statuses
        if order.table_id and order.table_id != order_update.table_id:
            # Release old table
            old_table = next((t for t in sample_tables if t.id == order.table_id), None)
            if old_table:
                old_table.is_occupied = False
                old_table.current_order_id = None
                old_table.status = "available"
                # Release all seats
                for seat in old_table.seats:
                    seat["status"] = "available"
                    seat["customer_name"] = None
        
        # Assign new table
        new_table = next((t for t in sample_tables if t.id == order_update.table_id), None)
        if new_table:
            new_table.is_occupied = True
            new_table.current_order_id = order_id
            new_table.status = "occupied"
            
            # Assign seats if provided
            if order_update.assigned_seats:
                for seat_num in order_update.assigned_seats:
                    if seat_num <= len(new_table.seats):
                        new_table.seats[seat_num-1]["status"] = "occupied"
        
        order.table_id = order_update.table_id
    
    if order_update.customer_count is not None:
        order.customer_count = order_update.customer_count
    
    if order_update.special_requests is not None:
        order.special_requests = order_update.special_requests
    
    if order_update.assigned_seats is not None:
        order.assigned_seats = order_update.assigned_seats
    
    # Update new order type fields if provided
    if order_update.order_type is not None:
        order.order_type = order_update.order_type
    
    if order_update.table_number is not None:
        order.table_number = order_update.table_number
    
    if order_update.customer_name is not None:
        order.customer_name = order_update.customer_name
    
    if order_update.customer_phone is not None:
        order.customer_phone = order_update.customer_phone
    
    if order_update.delivery_address is not None:
        order.delivery_address = order_update.delivery_address
    
    if order_update.modifiers is not None:
        order.modifiers = order_update.modifiers
    
    return order

@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: dict):
    """Update the status of an order"""
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Find the corresponding kitchen order
    kitchen_order = next((ko for ko in sample_kitchen_orders if ko.order_id == order_id), None)
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
        if new_status == "served" and order.order_type == "dine-in":
            # Release the table
            if order.table_id:
                table = next((t for t in sample_tables if t.id == order.table_id), None)
                if table:
                    table.is_occupied = False
                    table.current_order_id = None
                    table.status = "available"
                    # Release all seats
                    for seat in table.seats:
                        seat["status"] = "available"
                        seat["customer_name"] = None
    
    return order

@router.delete("/{order_id}")
def delete_order(order_id: int):
    """Delete an order"""
    global sample_orders
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # If order has an assigned table, release it
    if order.table_id:
        table = next((t for t in sample_tables if t.id == order.table_id), None)
        if table:
            table.is_occupied = False
            table.current_order_id = None
            table.status = "available"
            # Release all seats
            for seat in table.seats:
                seat["status"] = "available"
                seat["customer_name"] = None
    
    sample_orders = [o for o in sample_orders if o.id != order_id]
    return {"message": "Order deleted successfully"}

@router.post("/{order_id}/mark-served")
def mark_order_as_served(order_id: int):
    """Mark an order as served and release associated resources"""
    order = next((o for o in sample_orders if o.id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Find the corresponding kitchen order
    kitchen_order = next((ko for ko in sample_kitchen_orders if ko.order_id == order_id), None)
    if kitchen_order:
        # Update the kitchen order status to served
        kitchen_order.status = "served"
        kitchen_order.updated_at = datetime.now()
    
    # If it's a dine-in order, release the table
    if order.order_type == "dine-in":
        if order.table_id:
            table = next((t for t in sample_tables if t.id == order.table_id), None)
            if table:
                table.is_occupied = False
                table.current_order_id = None
                table.status = "available"
                # Release all seats
                for seat in table.seats:
                    seat["status"] = "available"
                    seat["customer_name"] = None
    
    return {"message": "Order marked as served", "order_id": order_id}