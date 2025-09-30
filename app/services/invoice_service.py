from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceItem
from app.models.order import Order
import json
from datetime import datetime
from typing import List

class InvoiceService:
    """Service class for handling invoice-related operations"""
    
    @staticmethod
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
    
    @staticmethod
    def create_invoice_from_order(db: Session, order_id: int) -> Invoice:
        """Create an invoice from an existing order"""
        # Check if order exists
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("Order not found")
        
        # Check if invoice already exists for this order
        existing_invoice = db.query(Invoice).filter(Invoice.order_id == order_id).first()
        if existing_invoice:
            raise ValueError("Invoice already exists for this order")
        
        # Parse order data
        try:
            order_data_value = getattr(order, 'order_data', None)
            order_items_data = json.loads(order_data_value) if order_data_value else []
        except (json.JSONDecodeError, Exception):
            order_items_data = []
        
        # Create invoice items from order items
        invoice_items = []
        for item_data in order_items_data:
            invoice_item = InvoiceItem(
                name=item_data.get('name', ''),
                category=item_data.get('category', ''),
                price=item_data.get('price', 0.0),
                quantity=1
            )
            invoice_items.append(invoice_item)
        
        # Generate unique invoice number
        invoice_number = InvoiceService.generate_invoice_number(db)
        
        # Determine payment type from order or default to cash
        payment_type = getattr(order, 'payment_type', 'cash')
        if payment_type is None:
            payment_type = 'cash'
        
        # Handle payment type conversion
        # We need to safely extract the value from an enum or use the string directly
        payment_type_value = str(payment_type)
        # If it's an enum, it will convert to its string representation
        # If it's already a string, it will remain unchanged
        
        # Create invoice record
        db_invoice = Invoice(
            invoice_number=invoice_number,
            order_id=order_id,
            customer_name=order.customer_name or '',
            customer_phone=order.customer_phone,
            customer_address=order.delivery_address,
            order_type=order.order_type or 'dine-in',
            table_number=order.table_number,
            subtotal=order.total or 0.0,
            tax=0.0,  # For simplicity, we'll assume 0 tax for now
            total=order.total or 0.0,
            invoice_data=json.dumps([item.dict() for item in invoice_items]),
            payment_type=payment_type_value
        )
        
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        
        return db_invoice
    
    @staticmethod
    def get_invoice_items(db: Session, invoice_id: int) -> List[InvoiceItem]:
        """Get invoice items for a specific invoice"""
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise ValueError("Invoice not found")
        
        try:
            invoice_data_value = getattr(invoice, 'invoice_data', None)
            items_data = json.loads(invoice_data_value) if invoice_data_value else []
            invoice_items = [InvoiceItem(**item_data) for item_data in items_data]
            return invoice_items
        except (json.JSONDecodeError, Exception):
            return []

# Create a singleton instance
invoice_service = InvoiceService()