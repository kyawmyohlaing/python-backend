import sys
import os

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import Base, engine
    from app.models.menu import MenuItem
    from app.models.user import User
    from app.config import Config
    from app.models.order import Order
    from app.models.order_item import OrderItem
    # Import our security module for password handling
    from app.security import hash_password
except ImportError:
    # Try importing directly (Docker container)
    from database import Base, engine
    from models import MenuItem
    from models import User
    from config import Config
    from models import Order
    from models import OrderItem
    # Import our security module for password handling
    from security import hash_password

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from passlib.context import CryptContext

def init_db():
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
                print('Adding sample user...')
                # Add a sample user (in a real application, you'd want to hash the password)
                pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
                
                sample_user = User(
                    username='admin',
                    email='admin@example.com',
                    hashed_password=hash_password('admin123'),
                    role='admin'
                )
                
                db.add(sample_user)
                db.commit()
                print('Sample user added successfully.')
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
    init_db()