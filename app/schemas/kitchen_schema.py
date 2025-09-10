from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .menu_schema import MenuItemBase

class KitchenOrderBase(BaseModel):
    order_id: int
    status: str = "pending"

class KitchenOrderCreate(KitchenOrderBase):
    pass

class KitchenOrderUpdate(BaseModel):
    status: str

class KitchenOrderResponse(KitchenOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class KitchenOrderDetail(BaseModel):
    id: int
    order_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: List[MenuItemBase]
    total: float

    class Config:
        from_attributes = True