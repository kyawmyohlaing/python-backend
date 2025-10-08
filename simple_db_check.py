#!/usr/bin/env python3
"""
Simple script to check database connection
"""

import sys
import os

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import engine
    from app.models.user import User
except ImportError:
    # Try importing directly (Docker container)
    from database import engine
    from models import User

from sqlalchemy.orm import sessionmaker

def check_db():
    try:
        print("Attempting to connect to database...")
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Try a simple query
        count = db.query(User).count()
        print(f"Database connection successful. Found {count} users.")
        
        db.close()
        
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_db()