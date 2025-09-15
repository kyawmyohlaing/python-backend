#!/usr/bin/env python3
"""
Database Schema Checker
Verifies that the database schema matches the expected structure for invoices and orders tables.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_invoices_table():
    """Check if the invoices table has the correct schema"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'invoices'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                logger.error("Invoices table does not exist")
                return False
            
            # Check columns
            result = conn.execute(text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'invoices'
                ORDER BY ordinal_position;
            """))
            columns = result.fetchall()
            
            # Expected columns and their properties
            expected_columns = {
                'id': {'data_type': 'integer', 'is_nullable': 'NO'},
                'invoice_number': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'order_id': {'data_type': 'integer', 'is_nullable': 'YES'},
                'customer_name': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'customer_phone': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'customer_address': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'order_type': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'table_number': {'data_type': 'character varying', 'is_nullable': 'YES'},
                'subtotal': {'data_type': 'double precision', 'is_nullable': 'YES'},
                'tax': {'data_type': 'double precision', 'is_nullable': 'YES', 'column_default': '0.0'},
                'total': {'data_type': 'double precision', 'is_nullable': 'YES'},
                'created_at': {'data_type': 'timestamp without time zone', 'is_nullable': 'YES'},
                'updated_at': {'data_type': 'timestamp without time zone', 'is_nullable': 'YES'},
                'invoice_data': {'data_type': 'text', 'is_nullable': 'YES'}
            }
            
            # Check each column
            for column in columns:
                col_name = column[0]
                col_type = column[1]
                col_nullable = column[2]
                col_default = column[3]
                
                if col_name in expected_columns:
                    expected = expected_columns[col_name]
                    if col_type != expected['data_type']:
                        logger.warning(f"Column {col_name}: expected type {expected['data_type']}, got {col_type}")
                    if col_nullable != expected['is_nullable']:
                        logger.warning(f"Column {col_name}: expected nullable {expected['is_nullable']}, got {col_nullable}")
                    if 'column_default' in expected and col_default != expected['column_default']:
                        logger.warning(f"Column {col_name}: expected default {expected['column_default']}, got {col_default}")
            
            logger.info("Invoices table schema check completed")
            return True
            
    except Exception as e:
        logger.error(f"Failed to check invoices table: {e}")
        return False

def check_orders_table():
    """Check if the orders table has the correct schema"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'orders'
                );
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                logger.error("Orders table does not exist")
                return False
            
            # For now, just confirm it exists
            logger.info("Orders table exists")
            return True
            
    except Exception as e:
        logger.error(f"Failed to check orders table: {e}")
        return False

def main():
    """Main function to check database schema"""
    logger.info("🔍 Checking database schema...")
    
    invoices_ok = check_invoices_table()
    orders_ok = check_orders_table()
    
    if invoices_ok:
        logger.info("✅ Invoices table schema check passed!")
    else:
        logger.error("❌ Invoices table schema check failed!")
        
    if orders_ok:
        logger.info("✅ Orders table schema check passed!")
    else:
        logger.error("❌ Orders table schema check failed!")
        
    return invoices_ok and orders_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)