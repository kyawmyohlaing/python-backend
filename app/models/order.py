from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .menu import MenuItemBase

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # Store order items as JSON string
    order_data = Column(Text)

# Pydantic models for API validation
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