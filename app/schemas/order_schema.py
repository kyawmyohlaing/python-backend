from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .menu_schema import MenuItemBase

class OrderItem(MenuItemBase):
    pass

class OrderBase(BaseModel):
    order: List[OrderItem]
    total: float
    table_id: Optional[int] = None
    customer_count: Optional[int] = 1
    special_requests: Optional[str] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    table_id: Optional[int] = None
    customer_count: Optional[int] = None
    special_requests: Optional[str] = None
    order: Optional[List[OrderItem]] = None
    total: Optional[float] = None

class OrderResponse(OrderBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True