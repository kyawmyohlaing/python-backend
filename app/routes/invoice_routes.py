from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime, timezone

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceItem
    from app.models.order import Order  # Import database Order model
    from app.services.invoice_service import invoice_service
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceItem
    from models.order import Order  # Import database Order model
    from services.invoice_service import invoice_service

router = APIRouter(prefix="/api/invoices", tags=["Invoices"])

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Retrieve all invoices"""
    invoices = db.query(Invoice).offset(skip).limit(limit).all()
    return [InvoiceResponse.from_orm(invoice) for invoice in invoices]

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a specific invoice by ID"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceResponse.from_orm(invoice)

@router.get("/order/{order_id}", response_model=InvoiceResponse)
def get_invoice_by_order_id(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve an invoice by order ID"""
    invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for this order")
    return InvoiceResponse.from_orm(invoice)

@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    """Create a new invoice"""
    # Check if order exists
    order = db.query(Order).filter(Order.id == invoice.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if invoice already exists for this order
    existing_invoice = db.query(Invoice).filter(Invoice.order_id == invoice.order_id).first()
    if existing_invoice:
        raise HTTPException(status_code=400, detail="Invoice already exists for this order")
    
    # Generate unique invoice number
    invoice_number = invoice_service.generate_invoice_number(db)
    
    # Convert invoice items to JSON string
    invoice_data_json = json.dumps([item.dict() for item in invoice.invoice_items])
    
    # Handle payment type
    payment_type = invoice.payment_type
    if payment_type:
        # Validate payment type
        valid_payment_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
        if payment_type not in valid_payment_types:
            payment_type = "cash"  # Default to cash if invalid
    
    # Create invoice record
    db_invoice = Invoice(
        invoice_number=invoice_number,
        order_id=invoice.order_id,
        customer_name=invoice.customer_name,
        customer_phone=invoice.customer_phone,
        customer_address=invoice.customer_address,
        order_type=invoice.order_type,
        table_number=invoice.table_number,
        subtotal=invoice.subtotal,
        tax=invoice.tax,
        total=invoice.total,
        invoice_data=invoice_data_json,
        payment_type=payment_type
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    return InvoiceResponse.from_orm(db_invoice)

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing invoice"""
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Update invoice fields
    update_data = invoice_update.dict(exclude_unset=True)
    
    # Handle special field for invoice items
    if "invoice_items" in update_data and update_data["invoice_items"] is not None:
        update_data['invoice_data'] = json.dumps([item.dict() for item in update_data["invoice_items"]])
        # Remove from update_data to avoid double processing
        del update_data["invoice_items"]
    
    # Handle payment_type validation
    if "payment_type" in update_data and update_data["payment_type"] is not None:
        payment_type = update_data["payment_type"]
        # Validate payment type
        valid_payment_types = ["cash", "card", "qr", "e_wallet", "gift_card"]
        if payment_type in valid_payment_types:
            update_data['payment_type'] = payment_type
        else:
            update_data['payment_type'] = "cash"
        del update_data["payment_type"]
    
    # Update remaining fields
    for key, value in update_data.items():
        setattr(db_invoice, key, value)
    
    db.commit()
    db.refresh(db_invoice)
    
    return InvoiceResponse.from_orm(db_invoice)

@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    """Delete an invoice"""
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(db_invoice)
    db.commit()
    return {"message": "Invoice deleted successfully"}