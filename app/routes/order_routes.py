from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
from database import get_db
from models.order import Order, OrderCreate, OrderUpdate, OrderResponse
from models.menu import MenuItem
from models.kitchen import KitchenOrderCreate, KitchenOrderResponse
from models.table import TableResponse
from data.shared_data import sample_orders, sample_kitchen_orders, sample_tables

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
    new_order = OrderResponse(
        id=new_id,
        order=order.order,
        total=order.total,
        table_id=order.table_id,
        customer_count=order.customer_count,
        special_requests=order.special_requests,
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
    
    # If table is assigned, update table status
    if order.table_id:
        table = next((t for t in sample_tables if t.id == order.table_id), None)
        if table:
            table.is_occupied = True
            table.current_order_id = new_id
            table.status = "occupied"
    
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
        
        # Assign new table
        new_table = next((t for t in sample_tables if t.id == order_update.table_id), None)
        if new_table:
            new_table.is_occupied = True
            new_table.current_order_id = order_id
            new_table.status = "occupied"
        
        order.table_id = order_update.table_id
    
    if order_update.customer_count is not None:
        order.customer_count = order_update.customer_count
    
    if order_update.special_requests is not None:
        order.special_requests = order_update.special_requests
    
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
    
    sample_orders = [o for o in sample_orders if o.id != order_id]
    return {"message": "Order deleted successfully"}