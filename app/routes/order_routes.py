from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
from database import get_db
from models.order import Order, OrderCreate, OrderResponse
from models.menu import MenuItem
from models.kitchen import KitchenOrderCreate, KitchenOrderResponse
from data.shared_data import sample_orders, sample_kitchen_orders

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderResponse])
def get_orders():
    """Get all orders"""
    return sample_orders

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate):
    """Create a new order"""
    # In a real application, this would save to the database
    new_id = len(sample_orders) + 1
    new_order = OrderResponse(
        id=new_id,
        order=order.order,
        total=order.total,
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
    
    return new_order