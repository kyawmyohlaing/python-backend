import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.menu import MenuItem

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

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_menu_item():
    """Test creating a new menu item"""
    response = client.post("/api/menu/", json={
        "name": "Test Item",
        "price": 5.99,
        "category": "Test Category"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 5.99
    assert data["category"] == "Test Category"
    assert "id" in data

def test_create_duplicate_menu_item():
    """Test creating a duplicate menu item should fail"""
    # First creation
    client.post("/api/menu/", json={
        "name": "Duplicate Test",
        "price": 5.99,
        "category": "Test Category"
    })
    
    # Second creation with same name should fail
    response = client.post("/api/menu/", json={
        "name": "Duplicate Test",
        "price": 6.99,
        "category": "Test Category"
    })
    assert response.status_code == 400

def test_get_menu_items():
    """Test getting all menu items"""
    # Create a few items
    client.post("/api/menu/", json={"name": "Item 1", "price": 1.0, "category": "Category 1"})
    client.post("/api/menu/", json={"name": "Item 2", "price": 2.0, "category": "Category 2"})
    
    response = client.get("/api/menu/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

def test_get_menu_item():
    """Test getting a specific menu item"""
    # Create an item
    create_response = client.post("/api/menu/", json={
        "name": "Specific Item",
        "price": 3.99,
        "category": "Specific Category"
    })
    item_id = create_response.json()["id"]
    
    # Get the item
    response = client.get(f"/api/menu/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Specific Item"
    assert data["price"] == 3.99

def test_get_nonexistent_menu_item():
    """Test getting a nonexistent menu item should fail"""
    response = client.get("/api/menu/99999")
    assert response.status_code == 404

def test_update_menu_item():
    """Test updating a menu item"""
    # Create an item
    create_response = client.post("/api/menu/", json={
        "name": "Original Item",
        "price": 4.99,
        "category": "Original Category"
    })
    item_id = create_response.json()["id"]
    
    # Update the item
    response = client.put(f"/api/menu/{item_id}", json={
        "name": "Updated Item",
        "price": 5.99,
        "category": "Updated Category"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 5.99
    assert data["category"] == "Updated Category"

def test_update_menu_item_to_duplicate_name():
    """Test updating a menu item to have a duplicate name should fail"""
    # Create two items
    item1_response = client.post("/api/menu/", json={
        "name": "Item 1",
        "price": 1.0,
        "category": "Category"
    })
    item1_id = item1_response.json()["id"]
    
    client.post("/api/menu/", json={
        "name": "Item 2",
        "price": 2.0,
        "category": "Category"
    })
    
    # Try to update item1 to have the same name as item2
    response = client.put(f"/api/menu/{item1_id}", json={
        "name": "Item 2",
        "price": 1.0,
        "category": "Category"
    })
    assert response.status_code == 400

def test_delete_menu_item():
    """Test deleting a menu item"""
    # Create an item
    create_response = client.post("/api/menu/", json={
        "name": "Delete Item",
        "price": 1.99,
        "category": "Delete Category"
    })
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/menu/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Menu item deleted successfully"
    
    # Try to get the deleted item
    get_response = client.get(f"/api/menu/{item_id}")
    assert get_response.status_code == 404

def test_batch_create_menu_items():
    """Test creating multiple menu items in batch"""
    items = [
        {"name": "Batch Item 1", "price": 1.0, "category": "Batch"},
        {"name": "Batch Item 2", "price": 2.0, "category": "Batch"},
        {"name": "Batch Item 3", "price": 3.0, "category": "Batch"}
    ]
    
    response = client.post("/api/menu/batch", json=items)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Batch Item 1"

def test_get_menu_items_by_category():
    """Test getting menu items by category"""
    # Create items in different categories
    client.post("/api/menu/", json={"name": "Category A Item 1", "price": 1.0, "category": "Category A"})
    client.post("/api/menu/", json={"name": "Category A Item 2", "price": 2.0, "category": "Category A"})
    client.post("/api/menu/", json={"name": "Category B Item 1", "price": 3.0, "category": "Category B"})
    
    # Get items by category
    response = client.get("/api/menu/category/Category A")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    for item in data:
        assert item["category"] == "Category A"

def test_get_menu_categories():
    """Test getting all unique menu categories"""
    # Create items in different categories
    client.post("/api/menu/", json={"name": "Category Test 1", "price": 1.0, "category": "TestCategory1"})
    client.post("/api/menu/", json={"name": "Category Test 2", "price": 2.0, "category": "TestCategory2"})
    client.post("/api/menu/", json={"name": "Category Test 3", "price": 3.0, "category": "TestCategory1"})  # Duplicate category
    
    # Get all categories
    response = client.get("/api/menu/categories")
    assert response.status_code == 200
    data = response.json()
    assert "TestCategory1" in data
    assert "TestCategory2" in data
    # Should have 2 unique categories
    assert len(data) >= 2