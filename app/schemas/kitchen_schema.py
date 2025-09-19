from pydantic import BaseModel
from typing import List, Optional, Union
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
    # Add missing fields for order type, table number, and customer name
    order_type: Optional[str] = None
    table_number: Optional[Union[str, int]] = None
    customer_name: Optional[str] = None

    class Config:
        from_attributes = True