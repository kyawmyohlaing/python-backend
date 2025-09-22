#!/usr/bin/env python3
"""
Script to manually create the invoices table.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from database import Base, engine
from models import invoice
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_invoices_table():
    """Create the invoices table."""
    try:
        # Create only the invoices table
        invoice.Base.metadata.create_all(bind=engine, tables=[invoice.Invoice.__table__])
        logger.info("✅ Invoices table created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create invoices table: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Creating invoices table...")
    print()
    
    success = create_invoices_table()
    
    print()
    if success:
        print("✅ Invoices table creation completed successfully!")
    else:
        print("❌ Invoices table creation failed!")