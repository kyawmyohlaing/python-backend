import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User, UserRole
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_user_creation_with_role(setup_database, db_session):
    """Test creating a user with a specific role"""
    user_data = UserCreate(
        name="Test User",
        email="test@example.com",
        password="testpassword",
        role=UserRole.WAITER
    )
    
    user = UserService.create_user(db_session, user_data)
    
    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.role == UserRole.WAITER

def test_user_registration_api(setup_database):
    """Test user registration API endpoint with role"""
    response = client.post("/users/register", json={
        "name": "API Test User",
        "email": "api_test@example.com",
        "password": "testpassword",
        "role": "cashier"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test User"
    assert data["email"] == "api_test@example.com"
    assert data["role"] == "cashier"

def test_user_login_and_role_check(setup_database):
    """Test user login and role verification"""
    # First register a user
    register_response = client.post("/users/register", json={
        "name": "Login Test User",
        "email": "login_test@example.com",
        "password": "testpassword",
        "role": "manager"
    })
    
    assert register_response.status_code == 200
    
    # Then login
    login_response = client.post("/users/login", json={
        "email": "login_test@example.com",
        "password": "testpassword"
    })
    
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Test accessing protected endpoint with token
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_response = client.get("/users/me", headers=headers)
    
    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["role"] == "manager"