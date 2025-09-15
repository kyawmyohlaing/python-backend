#!/usr/bin/env python3
"""
Script to check database connection and schema.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.database import engine
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database_connection():
    """Check if we can connect to the database."""
    try:
        with engine.connect() as connection:
            # Execute a simple query
            result = connection.execute(text("SELECT sqlite_version();"))
            version = result.fetchone()
            logger.info(f"✅ Database connection successful! SQLite version: {version[0]}")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def list_tables():
    """List all tables in the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = result.fetchall()
            logger.info("Tables in the database:")
            for table in tables:
                logger.info(f"  - {table[0]}")
            return True
    except Exception as e:
        logger.error(f"Failed to list tables: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking database connection and tables...")
    print()
    
    connection_success = check_database_connection()
    print()
    tables_success = list_tables()
    
    print()
    if connection_success and tables_success:
        print("✅ Database check completed successfully!")
    else:
        print("❌ Database check failed!")