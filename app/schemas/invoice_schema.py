from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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
    payment_type: Optional[str] = "cash"

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
    payment_type: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: int
    invoice_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True