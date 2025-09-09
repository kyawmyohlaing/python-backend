import pytest
from fastapi.testclient import TestClient
# Since we're in the container and files are directly in /app, we import directly
from main import app
from database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def test_register_user():
    """Test registering a new user via API"""
    user_data = {
        "name": "API Test User",
        "email": "api_test@example.com",
        "password": "testpassword"
    }
    
    response = client.post("/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data  # Password should not be returned

def test_register_duplicate_user():
    """Test registering a user with duplicate email"""
    # First registration
    user_data = {
        "name": "Duplicate Test User",
        "email": "duplicate@example.com",
        "password": "testpassword"
    }
    
    response1 = client.post("/users/register", json=user_data)
    assert response1.status_code == 200
    
    # Second registration with same email should fail
    response2 = client.post("/users/register", json=user_data)
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]

def test_login_user():
    """Test logging in a user"""
    # First register a user
    user_data = {
        "name": "Login Test User",
        "email": "login_test@example.com",
        "password": "testpassword"
    }
    
    register_response = client.post("/users/register", json=user_data)
    assert register_response.status_code == 200
    
    # Then login
    login_data = {
        "email": "login_test@example.com",
        "password": "testpassword"
    }
    
    login_response = client.post("/users/login", json=login_data)
    assert login_response.status_code == 200
    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test logging in with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = client.post("/users/login", json=login_data)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]

def test_get_current_user():
    """Test getting current user with valid token"""
    # First register and login to get a token
    user_data = {
        "name": "Current User Test",
        "email": "current_user@example.com",
        "password": "testpassword"
    }
    
    register_response = client.post("/users/register", json=user_data)
    assert register_response.status_code == 200
    
    login_data = {
        "email": "current_user@example.com",
        "password": "testpassword"
    }
    
    login_response = client.post("/users/login", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Get current user with valid token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current_user@example.com"
    assert data["name"] == "Current User Test"

def test_get_current_user_invalid_token():
    """Test getting current user with invalid token"""
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert "Invalid token" in response.json()["detail"]

def test_list_users():
    """Test listing all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)