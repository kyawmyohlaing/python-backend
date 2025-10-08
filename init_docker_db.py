#!/usr/bin/env python3
"""
Script to initialize the Docker PostgreSQL database with test users
This script is designed to work when running outside of Docker containers
"""

import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

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

def init_docker_db():
    """Initialize the Docker database with test users"""
    try:
        # Import database components
        from app.database import Base, engine
        from app.models.user import User
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext
        
        print(f"Connecting to database: {engine.url}")
        print("This should connect to the Docker PostgreSQL database at localhost:5432")
        
        # Create tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
        
        # Create a session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if we have any users
        existing_users = db.query(User).count()
        if existing_users == 0:
            print("Adding test users...")
            
            # Password hashing context
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            # Add admin user
            admin_password = truncate_password_for_bcrypt("admin123")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=pwd_context.hash(admin_password),
                role="admin"
            )
            
            # Add manager user
            manager_password = truncate_password_for_bcrypt("manager123")
            manager_user = User(
                username="manager",
                email="manager@example.com",
                hashed_password=pwd_context.hash(manager_password),
                role="manager"
            )
            
            # Add waiter user
            waiter_password = truncate_password_for_bcrypt("waiter123")
            waiter_user = User(
                username="waiter",
                email="waiter@example.com",
                hashed_password=pwd_context.hash(waiter_password),
                role="waiter"
            )
            
            db.add(admin_user)
            db.add(manager_user)
            db.add(waiter_user)
            db.commit()
            
            print("✅ Test users added successfully:")
            print("  - Admin: admin@example.com / admin123")
            print("  - Manager: manager@example.com / manager123")
            print("  - Waiter: waiter@example.com / waiter123")
        else:
            print(f"Database already contains {existing_users} users. Skipping user insertion.")
            
        db.close()
        print("✅ Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Docker is installed and running")
        print("2. Ensure the PostgreSQL container is running: docker-compose up -d db")
        print("3. Check if port 5432 is available")
        print("4. Verify database credentials match docker-compose.yml")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_docker_db()