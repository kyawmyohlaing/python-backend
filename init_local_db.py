#!/usr/bin/env python3
"""
Script to initialize the local SQLite database with sample data
"""

import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from passlib.context import CryptContext

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import models
from app.models.menu import MenuItem
from app.models.user import User, UserRole
from app.database import Base

def init_local_db():
    """Initialize the local SQLite database"""
    # Use the local SQLite database
    engine = create_engine("sqlite:///./app/dev.db")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have menu items
        try:
            existing_items = db.query(MenuItem).count()
            if existing_items == 0:
                print('Adding sample menu items...')
                # Add sample menu items
                sample_items = [
                    MenuItem(name='Burger', price=8.99, category='food'),
                    MenuItem(name='Pizza', price=12.99, category='food'),
                    MenuItem(name='Salad', price=7.99, category='food'),
                    MenuItem(name='Soda', price=2.99, category='drink'),
                    MenuItem(name='Coffee', price=3.99, category='drink'),
                    MenuItem(name='Tea Leaf Salad', price=6.99, category='food'),
                    MenuItem(name='Chicken Curry', price=11.99, category='food'),
                    MenuItem(name='Steak (Grill)', price=18.99, category='food'),
                    MenuItem(name='Wine', price=7.99, category='alcohol'),
                    MenuItem(name='Beer', price=5.99, category='alcohol'),
                ]
                
                for item in sample_items:
                    db.add(item)
                
                db.commit()
                print('Sample menu items added successfully.')
            else:
                print(f'Database already contains {existing_items} menu items. Skipping sample data insertion.')
        except ProgrammingError as e:
            print(f"Error querying menu items: {e}")
            db.rollback()
        
        # Check if we have any users
        try:
            existing_users = db.query(User).count()
            if existing_users == 0:
                print('Adding sample users...')
                # Add a sample users with different roles
                pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
                
                sample_users = [
                    User(
                        username='admin',
                        email='admin@example.com',
                        hashed_password=pwd_context.hash('admin123'),
                        role=UserRole.ADMIN
                    ),
                    User(
                        username='manager',
                        email='manager@example.com',
                        hashed_password=pwd_context.hash('manager123'),
                        role=UserRole.MANAGER
                    ),
                    User(
                        username='waiter',
                        email='waiter@example.com',
                        hashed_password=pwd_context.hash('waiter123'),
                        role=UserRole.WAITER
                    )
                ]
                
                for user in sample_users:
                    db.add(user)
                
                db.commit()
                print('Sample users added successfully.')
            else:
                print(f'Database already contains {existing_users} users. Skipping user insertion.')
        except ProgrammingError as e:
            print(f"Error querying users: {e}")
            db.rollback()
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        print('Database initialization completed successfully.')

if __name__ == "__main__":
    init_local_db()