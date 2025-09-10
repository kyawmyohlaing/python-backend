from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .menu import MenuItemBase

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # Store order items as JSON string
    order_data = Column(Text)
    # Table information
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=True)
    customer_count = Column(Integer, default=1)
    special_requests = Column(String, nullable=True)
    # Seat information
    assigned_seats = Column(String, nullable=True)  # JSON string of assigned seats

# Pydantic models for API validation
class OrderItem(MenuItemBase):
    pass

class OrderBase(BaseModel):
    order: List[OrderItem]
    total: float
    table_id: Optional[int] = None
    customer_count: Optional[int] = 1
    special_requests: Optional[str] = None
    assigned_seats: Optional[List[int]] = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    table_id: Optional[int] = None
    customer_count: Optional[int] = None
    special_requests: Optional[str] = None
    order: Optional[List[OrderItem]] = None
    total: Optional[float] = None
    assigned_seats: Optional[List[int]] = None

class OrderResponse(OrderBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True