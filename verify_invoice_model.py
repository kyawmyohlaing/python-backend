#!/usr/bin/env python3
"""
Simple verification script for invoice model
"""

def verify_invoice_model():
    """Verify that the invoice model can be imported and instantiated"""
    try:
        # Try to import the invoice model
        from app.models.invoice import Invoice, InvoiceItem, InvoiceBase
        print("✓ Invoice model imported successfully")
        
        # Try to import the invoice schema
        from app.schemas.invoice_schema import InvoiceCreate, InvoiceResponse
        print("✓ Invoice schema imported successfully")
        
        # Try to import the invoice routes
        from app.routes.invoice_routes import router
        print("✓ Invoice routes imported successfully")
        
        # Try to import the invoice service
        from app.services.invoice_service import invoice_service
        print("✓ Invoice service imported successfully")
        
        # Test creating an invoice item
        item = InvoiceItem(name="Test Item", category="Test", price=10.0)
        print(f"✓ InvoiceItem created: {item.name}")
        
        # Test creating an invoice base
        invoice_base = InvoiceBase(
            order_id=1,
            customer_name="Test Customer",
            order_type="dine-in",
            subtotal=10.0,
            total=10.0,
            invoice_items=[item]
        )
        print(f"✓ InvoiceBase created: {invoice_base.customer_name}")
        
        print("\nAll verifications passed! Invoice system is ready.")
        return True
        
    except Exception as e:
        print(f"✗ Error during verification: {str(e)}")
        return False

if __name__ == "__main__":
    verify_invoice_model()