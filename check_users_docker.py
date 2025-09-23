#!/usr/bin/env python3
"""
Script to check users in the database from within the Docker container.
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

def check_users():
    """Check if we can connect to the database and count users."""
    try:
        with engine.connect() as connection:
            # Count users
            result = connection.execute(text("SELECT COUNT(*) FROM users"))
            count = result.fetchone()[0]
            logger.info(f"✅ Database connection successful! Number of users: {count}")
            
            if count > 0:
                # Show first user (without password)
                result = connection.execute(text("SELECT id, username, email, role FROM users LIMIT 1"))
                user = result.fetchone()
                logger.info(f"Sample user: ID={user[0]}, Username={user[1]}, Email={user[2]}, Role={user[3]}")
            else:
                logger.info("No users found in the database")
            
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Checking database users...")
    print()
    
    success = check_users()
    
    print()
    if success:
        print("✅ Database user check completed successfully!")
    else:
        print("❌ Database user check failed!")