#!/usr/bin/env python3
"""
Script to create a manager user with a proper bcrypt hash
"""

import sys
import os
from datetime import datetime

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@db:5432/mydb'

def create_manager_user():
    """Create a manager user with a pre-computed bcrypt hash"""
    try:
        print("Creating manager user...")

        # Import required modules
        sys.path.append('/app')
        from app.database import engine
        from app.models.user import User, UserRole
        from sqlalchemy.orm import sessionmaker

        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Check if manager user already exists
        existing_user = db.query(User).filter(User.username == 'manager').first()
        if existing_user:
            print("Manager user already exists!")
            db.close()
            return

        # Use a pre-computed bcrypt hash for "manager123"
        # This is a known good hash for the password "manager123"
        hashed_password = "$2b$12$YljZqlQHihFUg5UuFya5VuNWMrvVvAcgk14hoq9j7DRHbqaZNggKe"
        
        print(f"Using pre-computed hash: {hashed_password}")

        # Create the manager user
        manager_user = User(
            username='manager',
            email='manager@example.com',
            hashed_password=hashed_password,
            role=UserRole.MANAGER
        )
        
        db.add(manager_user)
        db.commit()
        db.refresh(manager_user)

        print("✅ Manager user created successfully!")
        print(f"User ID: {manager_user.id}")
        print(f"Username: {manager_user.username}")
        print(f"Email: {manager_user.email}")
        print(f"Role: {manager_user.role}")
        print(f"Hashed password: {manager_user.hashed_password}")

        db.close()

    except Exception as e:
        print(f"Error creating manager user: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_manager_user()