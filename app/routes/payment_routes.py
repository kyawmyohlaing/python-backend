from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.order import Order
    from app.services.payment_service import payment_service
    from app.dependencies import get_current_user
    from app.models.user import User
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.order import Order
    from services.payment_service import payment_service
    from dependencies import get_current_user
    from models.user import User

router = APIRouter(prefix="/api/payments", tags=["Payments"])

# Pydantic models for request/response validation
class PaymentProcessRequest(BaseModel):
    order_id: int
    payment_type: str
    amount: float
    payment_details: Dict[str, Any] = {}

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
    reason: str = "Customer request"
    refund_details: Dict[str, Any] = {}

class RefundProcessResponse(BaseModel):
    success: bool
    order_id: int
    payment_type: str
    refunded_amount: float
    timestamp: datetime
    reference: str
    error: Optional[str] = None

class PaymentSummaryRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class PaymentTypeBreakdown(BaseModel):
    count: int
    amount: float

class PaymentSummaryResponse(BaseModel):
    success: bool
    total_revenue: float
    total_transactions: int
    payment_type_breakdown: Dict[str, PaymentTypeBreakdown]
    period: Dict[str, Optional[str]]
    error: Optional[str] = None

@router.post("/process", response_model=PaymentProcessResponse)
def process_payment(
    payment_request: PaymentProcessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Process a payment for an order
    """
    # Verify the order exists
    order = db.query(Order).filter(Order.id == payment_request.order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Prepare payment data
    payment_data = {
        "payment_type": payment_request.payment_type,
        "amount": payment_request.amount,
        "details": payment_request.payment_details
    }
    
    # Process the payment
    result = payment_service.process_payment(db, payment_request.order_id, payment_data)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return PaymentProcessResponse(**result)

@router.post("/refund", response_model=RefundProcessResponse)
def refund_payment(
    refund_request: RefundProcessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Process a refund for a paid order
    """
    # Process the refund
    result = payment_service.refund_payment(db, refund_request.order_id, {
        "reason": refund_request.reason,
        "details": refund_request.refund_details
    })
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return RefundProcessResponse(**result)

@router.get("/methods", response_model=Dict[str, Dict[str, Any]])
def get_payment_methods(
    current_user: User = Depends(get_current_user)
):
    """
    Get available payment methods
    """
    return payment_service.PAYMENT_METHODS

@router.post("/summary", response_model=PaymentSummaryResponse)
def get_payment_summary(
    summary_request: PaymentSummaryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get payment summary statistics
    """
    result = payment_service.get_payment_summary(
        db, 
        summary_request.start_date, 
        summary_request.end_date
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"]
        )
    
    return PaymentSummaryResponse(**result)

@router.get("/order/{order_id}", response_model=Dict[str, Any])
def get_order_payment_status(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get payment status for a specific order
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return {
        "order_id": order.id,
        "payment_status": getattr(order, 'payment_status', 'pending'),
        "payment_type": getattr(order, 'payment_type', 'cash'),
        "paid_at": getattr(order, 'paid_at', None),
        "refund_status": getattr(order, 'refund_status', None),
        "refunded_at": getattr(order, 'refunded_at', None)
    }