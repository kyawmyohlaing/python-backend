from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .menu import MenuItemBase


class KitchenOrderDetail(BaseModel):
    id: int
    order_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: List[MenuItemBase]
    total: float
    # New order type information fields
    order_type: Optional[str] = "dine-in"  # dine-in, takeaway, delivery
    table_number: Optional[str] = None
    customer_name: Optional[str] = None

    class Config:
        from_attributes = True


class KitchenOrder(Base):
    __tablename__ = "kitchen_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    status = Column(String, default="pending")  # pending, preparing, ready
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Pydantic models for API validation
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

