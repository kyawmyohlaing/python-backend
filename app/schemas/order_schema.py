from pydantic import BaseModel
from typing import List
from datetime import datetime
from .menu_schema import MenuItemBase

class OrderItem(MenuItemBase):
    pass

class OrderBase(BaseModel):
    order: List[OrderItem]
    total: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True