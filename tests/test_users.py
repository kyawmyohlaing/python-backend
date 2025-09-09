import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Since we're in the container and files are directly in /app, we import directly
from database import Base
from models.user import User
from schemas.user_schema import UserCreate
from services.user_service import UserService
from security import verify_password

@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing with SQLite in-memory database"""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user_service(db_session):
    """Test creating a new user with hashed password"""
    user_data = UserCreate(name="Test User", email="test@example.com", password="password123")
    user = UserService.create_user(db_session, user_data)
    
    # Refresh the user from the database to get actual values
    db_session.refresh(user)
    
    # Access attributes as strings to avoid type issues
    user_name = str(user.name)
    user_email = str(user.email)
    user_password = str(user.password)
    
    assert user_name == "Test User"
    assert user_email == "test@example.com"
    # Check that password is hashed
    assert user_password != "password123"
    assert verify_password("password123", user_password)

def test_authenticate_user(db_session):
    """Test user authentication"""
    # First create a user
    user_data = UserCreate(name="Test User", email="test@example.com", password="password123")
    user = UserService.create_user(db_session, user_data)
    
    # Refresh the user from the database
    db_session.refresh(user)
    
    # Then authenticate
    authenticated_user = UserService.authenticate_user(db_session, "test@example.com", "password123")
    assert authenticated_user is not None
    assert str(authenticated_user.email) == "test@example.com"
    
    # Test with wrong password
    authenticated_user = UserService.authenticate_user(db_session, "test@example.com", "wrongpassword")
    assert authenticated_user is None

def test_get_users(db_session):
    """Test retrieving all users"""
    # Create two users
    user_data1 = UserCreate(name="User 1", email="user1@example.com", password="password123")
    user_data2 = UserCreate(name="User 2", email="user2@example.com", password="password456")
    UserService.create_user(db_session, user_data1)
    UserService.create_user(db_session, user_data2)
    
    # Get all users
    users = UserService.get_users(db_session)
    assert len(users) == 2
    assert str(users[0].name) == "User 1"
    assert str(users[1].name) == "User 2"

def test_update_user(db_session):
    """Test updating user information"""
    # Create a user
    user_data = UserCreate(name="Original User", email="original@example.com", password="password123")
    user = UserService.create_user(db_session, user_data)
    
    # Update the user
    from schemas.user_schema import UserUpdate
    update_data = UserUpdate(name="Updated User")
    updated_user = UserService.update_user(db_session, user.id, update_data)
    
    assert updated_user is not None
    assert str(updated_user.name) == "Updated User"

def test_delete_user(db_session):
    """Test deleting a user"""
    # Create a user
    user_data = UserCreate(name="User to Delete", email="delete@example.com", password="password123")
    user = UserService.create_user(db_session, user_data)
    
    # Delete the user
    result = UserService.delete_user(db_session, user.id)
    assert result is True
    
    # Verify user is deleted
    deleted_user = UserService.get_user(db_session, user.id)
    assert deleted_user is None

if __name__ == "__main__":
    unittest.main()

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Since we're in the container and files are directly in /app, we import directly
from main import app
from database import Base, get_db
from schemas.user_schema import UserCreate as SchemaUserCreate

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user_via_api():
    """Test creating a new user via API endpoint"""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_get_user():
    """Test getting a user by ID"""
    # First create a user
    user_data = {
        "name": "Test User",
        "email": "test2@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    
    # Then get the user
    response = client.get(f"/api/v1/users/{created_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_user["id"]

def test_list_users():
    """Test listing users"""
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_user():
    """Test updating a user"""
    # First create a user
    user_data = {
        "name": "Test User",
        "email": "test3@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 200
    created_user = response.json()
    
    # Update the user
    update_data = {
        "name": "Updated User"
    }
    
    response = client.put(f"/api/v1/users/{created_user['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated User"