from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    customer_name = Column(String)
    customer_phone = Column(String, nullable=True)
    customer_address = Column(String, nullable=True)
    order_type = Column(String)  # dine-in, takeaway, delivery
    table_number = Column(String, nullable=True)
    subtotal = Column(Float)
    tax = Column(Float, default=0.0)
    total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Store invoice items as JSON string
    invoice_data = Column(Text)

# Pydantic models for API validation
class InvoiceItem(BaseModel):
    name: str
    category: str
    price: float
    quantity: int = 1

class InvoiceBase(BaseModel):
    order_id: int
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    order_type: str
    table_number: Optional[str] = None
    subtotal: float
    tax: float = 0.0
    total: float
    invoice_items: List[InvoiceItem]

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    invoice_items: Optional[List[InvoiceItem]] = None

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True