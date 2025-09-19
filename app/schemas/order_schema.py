from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from .menu_schema import MenuItemBase

class OrderItem(MenuItemBase):
    modifiers: Optional[List[str]] = []

class OrderBase(BaseModel):
    order: List[OrderItem]
    total: float
    table_id: Optional[int] = None
    customer_count: Optional[int] = 1
    special_requests: Optional[str] = None

class OrderCreate(OrderBase):
    assigned_seats: Optional[List[int]] = None
    order_type: Optional[str] = "dine_in"
    table_number: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    modifiers: Optional[dict] = None

class OrderUpdate(BaseModel):
    table_id: Optional[int] = None
    customer_count: Optional[int] = None
    special_requests: Optional[str] = None
    order: Optional[List[OrderItem]] = None
    total: Optional[float] = None
    assigned_seats: Optional[List[int]] = None
    order_type: Optional[str] = None
    table_number: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    modifiers: Optional[dict] = None

class OrderResponse(OrderBase):
    id: int
    timestamp: datetime
    order_type: Optional[str] = None
    table_number: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    delivery_address: Optional[str] = None
    assigned_seats: Optional[List[int]] = None
    modifiers: Optional[dict] = None

    class Config:
        from_attributes = True