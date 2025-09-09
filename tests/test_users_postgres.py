import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Since we're in the container and files are directly in /app, we import directly
from database import Base
from models.user import User
from schemas.user_schema import UserCreate
from services.user_service import UserService
from security import verify_password

# For PostgreSQL testing, you would set the TEST_DATABASE_URL environment variable
# Example: postgresql://postgres:password@localhost:5432/test_db
TEST_POSTGRES_URL = os.getenv("TEST_POSTGRES_URL", "")

@pytest.mark.skipif(not TEST_POSTGRES_URL, reason="PostgreSQL test database URL not provided")
def test_postgres_create_user():
    """Test creating a new user with hashed password in PostgreSQL"""
    engine = create_engine(TEST_POSTGRES_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        user_data = UserCreate(name="Postgres Test User", email="postgres_test@example.com", password="password123")
        user = UserService.create_user(db, user_data)
        
        assert str(user.name) == "Postgres Test User"
        assert str(user.email) == "postgres_test@example.com"
        # Check that password is hashed
        assert str(user.password) != "password123"
        assert verify_password("password123", str(user.password))
    finally:
        # Clean up - delete the test user
        db.query(User).filter(User.email == "postgres_test@example.com").delete()
        db.commit()
        db.close()

@pytest.mark.skipif(not TEST_POSTGRES_URL, reason="PostgreSQL test database URL not provided")
def test_postgres_authenticate_user():
    """Test user authentication with PostgreSQL"""
    engine = create_engine(TEST_POSTGRES_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        # First create a user
        user_data = UserCreate(name="Postgres Auth User", email="postgres_auth@example.com", password="password123")
        UserService.create_user(db, user_data)
        
        # Then authenticate
        user = UserService.authenticate_user(db, "postgres_auth@example.com", "password123")
        assert user is not None
        assert str(user.email) == "postgres_auth@example.com"
        
        # Test with wrong password
        user = UserService.authenticate_user(db, "postgres_auth@example.com", "wrongpassword")
        assert user is None
    finally:
        # Clean up - delete the test user
        db.query(User).filter(User.email == "postgres_auth@example.com").delete()
        db.commit()
        db.close()