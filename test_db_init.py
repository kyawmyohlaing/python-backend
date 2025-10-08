#!/usr/bin/env python3
"""
Script to test database initialization process
"""

import sys
import os

# Set the database URL to match the Docker environment
os.environ['DATABASE_URL'] = 'postgresql://postgres:password@localhost:5432/mydb'

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_db_init():
    """Test database initialization process"""
    try:
        print("Testing database initialization process...")
        
        # Import required modules
        from app.database import Base, engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext
        from app.models.user import UserRole
        
        print(f"Connecting to database: {engine.url}")
        
        # Create tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if we have any users
        existing_users = db.query(User).count()
        print(f"Existing users in database: {existing_users}")
        
        if existing_users == 0:
            print("Adding sample users...")
            
            # Password hashing context
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            # Define truncation function
            def truncate_password_for_bcrypt(password: str) -> str:
                """
                Truncate password to 72 bytes for bcrypt compatibility.
                Bcrypt has a limitation where only the first 72 bytes are used.
                """
                MAX_PASSWORD_LENGTH = 72
                if isinstance(password, str):
                    # Encode to bytes to check actual byte length
                    password_bytes = password.encode('utf-8')
                    if len(password_bytes) > MAX_PASSWORD_LENGTH:
                        # Truncate to 72 bytes and decode back to string
                        truncated_bytes = password_bytes[:MAX_PASSWORD_LENGTH]
                        return truncated_bytes.decode('utf-8', errors='ignore')
                return password
            
            # Add admin user
            admin_password = truncate_password_for_bcrypt("admin123")
            print(f"Admin password length: {len(admin_password)}")
            admin_hash = pwd_context.hash(admin_password)
            print(f"Admin hash length: {len(admin_hash)}")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=admin_hash,
                role=UserRole.ADMIN
            )
            
            # Add manager user
            manager_password = truncate_password_for_bcrypt("manager123")
            print(f"Manager password length: {len(manager_password)}")
            manager_hash = pwd_context.hash(manager_password)
            print(f"Manager hash length: {len(manager_hash)}")
            manager_user = User(
                username="manager",
                email="manager@example.com",
                hashed_password=manager_hash,
                role=UserRole.MANAGER
            )
            
            # Add waiter user
            waiter_password = truncate_password_for_bcrypt("waiter123")
            print(f"Waiter password length: {len(waiter_password)}")
            waiter_hash = pwd_context.hash(waiter_password)
            print(f"Waiter hash length: {len(waiter_hash)}")
            waiter_user = User(
                username="waiter",
                email="waiter@example.com",
                hashed_password=waiter_hash,
                role=UserRole.WAITER
            )
            
            sample_users = [admin_user, manager_user, waiter_user]
            
            for user in sample_users:
                print(f"Adding user: {user.username}")
                db.add(user)
            
            db.commit()
            print("Sample users added successfully.")
        else:
            print("Database already contains users. Checking them...")
            users = db.query(User).all()
            for user in users:
                print(f"User: {user.username}, Email: {user.email}, Role: {user.role}")
                print(f"  Password hash: {user.hashed_password}")
                print(f"  Password hash length: {len(str(user.hashed_password)) if user.hashed_password else 0}")
        
        db.close()
        print("Database initialization test completed successfully.")
        
    except Exception as e:
        print(f"Error during database initialization test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_db_init()