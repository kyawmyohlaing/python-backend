#!/usr/bin/env python3
"""
Simple test to verify SQLite database connection and table creation
"""

import sys
import os

# Load local environment variables
from dotenv import load_dotenv
load_dotenv('.env.local')

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_sqlite():
    """Test SQLite database connection"""
    try:
        # Import database components
        from app.database import Base, engine
        from app.models.user import User
        
        print(f"Database URL: {engine.url}")
        print(f"Database type: {engine.name}")
        
        # Create tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully.")
        
        # Test creating a user
        from sqlalchemy.orm import sessionmaker
        from passlib.context import CryptContext
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if we have any users
        existing_users = db.query(User).count()
        print(f"Existing users: {existing_users}")
        
        if existing_users == 0:
            print("Adding test user...")
            
            # Password hashing context
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            # Add test user
            test_user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=pwd_context.hash("test123"),
                role="admin"
            )
            
            db.add(test_user)
            db.commit()
            print("✅ Test user added successfully.")
            
            # Verify user was added
            user_count = db.query(User).count()
            print(f"Users after adding: {user_count}")
        
        db.close()
        print("✅ SQLite test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing SQLite: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sqlite()