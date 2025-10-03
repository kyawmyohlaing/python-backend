from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime

class PaymentMethodBase(BaseModel):
    name: str
    requires_processing: bool
    instant_confirmation: bool

class PaymentProcessRequest(BaseModel):
    order_id: int
    payment_type: str
    amount: float
    payment_details: Optional[Dict[str, Any]] = {}

class PaymentProcessResponse(BaseModel):
    success: bool
    order_id: int
    payment_type: str
    amount: float
    timestamp: datetime
    invoice_id: Optional[int] = None
    error: Optional[str] = None

class RefundProcessRequest(BaseModel):
    order_id: int
    reason: Optional[str] = "Customer request"
    refund_details: Optional[Dict[str, Any]] = {}

class RefundProcessResponse(BaseModel):
    success: bool
    order_id: int
    payment_type: str
    refunded_amount: float
    timestamp: datetime
    reference: str
    error: Optional[str] = None

class PaymentTypeBreakdown(BaseModel):
    count: int
    amount: float

class PaymentSummaryRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class PaymentSummaryResponse(BaseModel):
    success: bool
    total_revenue: float
    total_transactions: int
    payment_type_breakdown: Dict[str, PaymentTypeBreakdown]
    period: Dict[str, Optional[str]]
    error: Optional[str] = None

class OrderPaymentStatus(BaseModel):
    order_id: int
    payment_status: Optional[str] = "pending"
    payment_type: Optional[str] = "cash"
    paid_at: Optional[datetime] = None
    refund_status: Optional[str] = None
    refunded_at: Optional[datetime] = None

class PaymentMethodsResponse(BaseModel):
    payment_methods: Dict[str, PaymentMethodBase]