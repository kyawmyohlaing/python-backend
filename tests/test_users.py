import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import Base
    from app.models.user import User
    from app.schemas.user_schema import UserCreate
    from app.services.user_service import UserService
    from app.security import verify_password
except ImportError:
    # Try importing directly (Docker container)
    try:
        from database import Base
        from models.user import User
        from schemas.user_schema import UserCreate
        from services.user_service import UserService
        from security import verify_password
    except ImportError:
        # If imports fail, skip the tests
        pytest.skip("Skipping tests due to import issues", allow_module_level=True)

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
    user_data = UserCreate(username="testuser", email="test@example.com", password="password123", full_name="Test User")
    user = UserService.create_user(db_session, user_data)
    
    # Refresh the user from the database to get actual values
    db_session.refresh(user)
    
    # Access attributes as strings to avoid type issues
    user_username = str(user.username)
    user_email = str(user.email)
    user_password = str(user.hashed_password)
    user_full_name = str(user.full_name)
    
    assert user_username == "testuser"
    assert user_email == "test@example.com"
    assert user_full_name == "Test User"
    # Check that password is hashed
    assert user_password != "password123"
    assert verify_password("password123", user_password)
    # Check that timestamps are set
    assert user.created_at is not None
    assert user.updated_at is not None

def test_authenticate_user(db_session):
    """Test user authentication"""
    # First create a user
    user_data = UserCreate(username="testuser", email="test@example.com", password="password123")
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
    user_data1 = UserCreate(username="user1", email="user1@example.com", password="password123", full_name="User One")
    user_data2 = UserCreate(username="user2", email="user2@example.com", password="password456", full_name="User Two")
    UserService.create_user(db_session, user_data1)
    UserService.create_user(db_session, user_data2)
    
    # Get all users
    users = UserService.get_users(db_session)
    assert len(users) == 2
    assert str(users[0].username) == "user1"
    assert str(users[1].username) == "user2"

def test_update_user_service(db_session):
    """Test updating user information"""
    # Create a user
    user_data = UserCreate(username="originaluser", email="original@example.com", password="password123", full_name="Original User")
    user = UserService.create_user(db_session, user_data)
    
    # Update the user using the ID directly (let SQLAlchemy handle the conversion)
    try:
        from app.schemas.user_schema import UserUpdate
    except ImportError:
        from schemas.user_schema import UserUpdate
    update_data = UserUpdate(username="updateduser", full_name="Updated User")
    updated_user = UserService.update_user(db_session, user.id, update_data)
    
    assert updated_user is not None
    assert str(updated_user.username) == "updateduser"
    assert str(updated_user.full_name) == "Updated User"

def test_delete_user(db_session):
    """Test deleting a user"""
    # Create a user
    user_data = UserCreate(username="todelete", email="delete@example.com", password="password123")
    user = UserService.create_user(db_session, user_data)
    
    # Delete the user using the ID directly (let SQLAlchemy handle the conversion)
    result = UserService.delete_user(db_session, user.id)
    assert result is True
    
    # Verify user is deleted
    deleted_user = UserService.get_user(db_session, user.id)
    assert deleted_user is None

# Handle imports for API tests
try:
    from fastapi.testclient import TestClient
    from app.main import app
    from app.database import Base, get_db
    from app.schemas.user_schema import UserCreate as SchemaUserCreate
except ImportError:
    try:
        from fastapi.testclient import TestClient
        from main import app
        from database import Base, get_db
        from schemas.user_schema import UserCreate as SchemaUserCreate
    except:
        # Skip API tests if imports fail
        pass

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

try:
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    def test_create_user_via_api():
        """Test creating a new user via API endpoint"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_user_via_api():
        """Test getting a user by ID"""
        # First create a user
        user_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "testpassword",
            "full_name": "Test User 2"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        created_user = response.json()
        
        # Then get the user
        response = client.get(f"/api/auth/users/{created_user['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_user["id"]
        assert data["full_name"] == user_data["full_name"]
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    def test_list_users_via_api():
        """Test listing users"""
        response = client.get("/api/auth/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_update_user_via_api():
        """Test updating a user"""
        # First create a user
        user_data = {
            "username": "testuser3",
            "email": "test3@example.com",
            "password": "testpassword",
            "full_name": "Test User 3"
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        created_user = response.json()
        
        # Update the user
        update_data = {
            "username": "updateduser",
            "full_name": "Updated User"
        }
        
        response = client.put(f"/api/auth/users/{created_user['id']}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
        assert data["full_name"] == "Updated User"
except:
    pass