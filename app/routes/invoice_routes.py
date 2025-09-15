from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime
from database import get_db
from models.invoice import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceResponse, InvoiceItem
from models.order import Order

router = APIRouter(prefix="/api/invoices", tags=["Invoices"])

def generate_invoice_number(db: Session) -> str:
    """Generate a unique invoice number"""
    # Get the current year and month
    now = datetime.now()
    year_month = now.strftime("%Y%m")
    
    # Count existing invoices for this month
    invoice_count = db.query(Invoice).filter(
        Invoice.invoice_number.like(f"INV-{year_month}%")
    ).count()
    
    # Generate invoice number in format: INV-YYYYMM-XXXX
    invoice_number = f"INV-{year_month}-{invoice_count + 1:04d}"
    return invoice_number

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(db: Session = Depends(get_db)):
    """Get all invoices"""
    invoices = db.query(Invoice).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get a specific invoice by ID"""
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """Create a new invoice from an order"""
    # Check if order exists
    order = db.query(Order).filter(Order.id == invoice.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if invoice already exists for this order
    existing_invoice = db.query(Invoice).filter(Invoice.order_id == invoice.order_id).first()
    if existing_invoice:
        raise HTTPException(status_code=400, detail="Invoice already exists for this order")
    
    # Generate unique invoice number
    invoice_number = generate_invoice_number(db)
    
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
        invoice_data=json.dumps([item.dict() for item in invoice.invoice_items])
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    return db_invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(invoice_id: int, invoice_update: InvoiceUpdate, db: Session = Depends(get_db)):
    """Update an existing invoice"""
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Update invoice fields if provided
    if invoice_update.customer_name is not None:
        db_invoice.customer_name = invoice_update.customer_name
    
    if invoice_update.customer_phone is not None:
        db_invoice.customer_phone = invoice_update.customer_phone
    
    if invoice_update.customer_address is not None:
        db_invoice.customer_address = invoice_update.customer_address
    
    if invoice_update.subtotal is not None:
        db_invoice.subtotal = invoice_update.subtotal
    
    if invoice_update.tax is not None:
        db_invoice.tax = invoice_update.tax
    
    if invoice_update.total is not None:
        db_invoice.total = invoice_update.total
    
    if invoice_update.invoice_items is not None:
        db_invoice.invoice_data = json.dumps([item.dict() for item in invoice_update.invoice_items])
    
    db_invoice.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_invoice)
    
    return db_invoice

@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Delete an invoice"""
    db_invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not db_invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(db_invoice)
    db.commit()
    
    return {"message": "Invoice deleted successfully"}

@router.get("/order/{order_id}", response_model=InvoiceResponse)
def get_invoice_by_order(order_id: int, db: Session = Depends(get_db)):
    """Get invoice by order ID"""
    invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found for this order")
    return invoice