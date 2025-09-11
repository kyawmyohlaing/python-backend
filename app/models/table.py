from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Table(Base):
    __tablename__ = "tables"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer, unique=True, index=True)
    capacity = Column(Integer)
    is_occupied = Column(Boolean, default=False)
    current_order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    status = Column(String, default="available")  # available, occupied, reserved, cleaning
    seats = Column(JSON, default=[])  # Track individual seats and their status

# Pydantic models for API validation
class TableBase(BaseModel):
    table_number: int
    capacity: int

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    is_occupied: Optional[bool] = None
    current_order_id: Optional[int] = None
    status: Optional[str] = None
    seats: Optional[List[dict]] = None

class TableResponse(TableBase):
    id: int
    is_occupied: bool
    current_order_id: Optional[int] = None
    status: str
    seats: Optional[List[dict]] = None

    class Config:
        from_attributes = True

class TableWithOrderDetails(TableResponse):
    order_details: Optional[dict] = None

    class Config:
        from_attributes = True