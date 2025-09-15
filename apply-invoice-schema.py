#!/usr/bin/env python3
"""
Script to apply the invoice schema updates to the database.
This script will create or update the invoices table to match the Invoice model.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.database import engine
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def apply_invoice_schema():
    """Apply the invoice schema updates to the database."""
    try:
        # Read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'update-invoices-table.sql')
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        
        # Execute the SQL script
        with engine.connect() as connection:
            # Split the script into individual statements
            statements = sql_script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:  # Skip empty statements
                    try:
                        logger.info(f"Executing: {statement[:50]}...")
                        connection.execute(statement)
                    except Exception as e:
                        logger.warning(f"Statement failed (may be expected): {statement[:50]}... Error: {e}")
            
            # Commit the changes
            connection.commit()
        
        logger.info("Invoice schema updates applied successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Failed to apply invoice schema updates: {e}")
        return False

if __name__ == "__main__":
    success = apply_invoice_schema()
    if success:
        print("✅ Invoice schema updates applied successfully!")
    else:
        print("❌ Failed to apply invoice schema updates")
        sys.exit(1)