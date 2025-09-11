import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

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

def test_create_dine_in_order_with_modifiers():
    """Test creating a dine-in order with modifiers"""
    # First, let's get the menu items to use in our order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    # Create a dine-in order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["no onions", "extra cheese"]
            }
        ],
        "total": menu_items[0]["price"],
        "order_type": "dine-in",
        "table_number": "5",
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890"
    }
    
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response contains the expected data
    assert data["order_type"] == "dine-in"
    assert data["table_number"] == "5"
    assert data["customer_name"] == "John Doe"
    assert data["customer_phone"] == "123-456-7890"
    assert len(data["order"]) == 1
    assert data["order"][0]["modifiers"] == ["no onions", "extra cheese"]
    assert data["total"] == menu_items[0]["price"]

def test_create_takeaway_order_with_modifiers():
    """Test creating a takeaway order with modifiers"""
    # First, let's get the menu items to use in our order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    # Create a takeaway order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[1]["name"],
                "price": menu_items[1]["price"],
                "category": menu_items[1]["category"],
                "modifiers": ["extra spicy"]
            },
            {
                "name": menu_items[2]["name"],
                "price": menu_items[2]["price"],
                "category": menu_items[2]["category"],
                "modifiers": ["no peanuts"]
            }
        ],
        "total": menu_items[1]["price"] + menu_items[2]["price"],
        "order_type": "takeaway",
        "customer_name": "Jane Smith",
        "customer_phone": "987-654-3210"
    }
    
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response contains the expected data
    assert data["order_type"] == "takeaway"
    assert data["customer_name"] == "Jane Smith"
    assert data["customer_phone"] == "987-654-3210"
    assert len(data["order"]) == 2
    assert data["order"][0]["modifiers"] == ["extra spicy"]
    assert data["order"][1]["modifiers"] == ["no peanuts"]
    assert data["total"] == menu_items[1]["price"] + menu_items[2]["price"]

def test_create_delivery_order_with_modifiers():
    """Test creating a delivery order with modifiers"""
    # First, let's get the menu items to use in our order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    # Create a delivery order with modifiers
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["no onions"]
            },
            {
                "name": menu_items[3]["name"],
                "price": menu_items[3]["price"],
                "category": menu_items[3]["category"],
                "modifiers": ["extra cheese", "well done"]
            }
        ],
        "total": menu_items[0]["price"] + menu_items[3]["price"],
        "order_type": "delivery",
        "customer_name": "Bob Johnson",
        "customer_phone": "555-123-4567",
        "delivery_address": "123 Main St, City, State 12345"
    }
    
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response contains the expected data
    assert data["order_type"] == "delivery"
    assert data["customer_name"] == "Bob Johnson"
    assert data["customer_phone"] == "555-123-4567"
    assert data["delivery_address"] == "123 Main St, City, State 12345"
    assert len(data["order"]) == 2
    assert data["order"][0]["modifiers"] == ["no onions"]
    assert data["order"][1]["modifiers"] == ["extra cheese", "well done"]
    assert data["total"] == menu_items[0]["price"] + menu_items[3]["price"]

def test_get_orders():
    """Test retrieving all orders"""
    response = client.get("/api/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # We should have at least the orders we created in the previous tests
    assert len(data) >= 3

def test_get_order_by_id():
    """Test retrieving a specific order by ID"""
    # First create an order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["test modifier"]
            }
        ],
        "total": menu_items[0]["price"],
        "order_type": "takeaway",
        "customer_name": "Test Customer",
        "customer_phone": "111-222-3333"
    }
    
    create_response = client.post("/api/orders", json=order_data)
    assert create_response.status_code == 200
    created_order = create_response.json()
    
    # Now retrieve the order by ID
    response = client.get(f"/api/orders/{created_order['id']}")
    assert response.status_code == 200
    data = response.json()
    
    # Verify the retrieved order matches what we created
    assert data["id"] == created_order["id"]
    assert data["order_type"] == "takeaway"
    assert data["customer_name"] == "Test Customer"
    assert data["customer_phone"] == "111-222-3333"
    assert len(data["order"]) == 1
    assert data["order"][0]["modifiers"] == ["test modifier"]

def test_update_order_with_modifiers():
    """Test updating an order with modifiers"""
    # First create an order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["original modifier"]
            }
        ],
        "total": menu_items[0]["price"],
        "order_type": "dine-in",
        "table_number": "10",
        "customer_name": "Original Customer"
    }
    
    create_response = client.post("/api/orders", json=order_data)
    assert create_response.status_code == 200
    created_order = create_response.json()
    
    # Now update the order
    update_data = {
        "order_type": "takeaway",
        "customer_name": "Updated Customer",
        "customer_phone": "999-888-7777",
        "order": [
            {
                "name": menu_items[1]["name"],
                "price": menu_items[1]["price"],
                "category": menu_items[1]["category"],
                "modifiers": ["updated modifier", "extra sauce"]
            }
        ],
        "total": menu_items[1]["price"]
    }
    
    response = client.put(f"/api/orders/{created_order['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    
    # Verify the updated order contains the new data
    assert data["order_type"] == "takeaway"
    assert data["customer_name"] == "Updated Customer"
    assert data["customer_phone"] == "999-888-7777"
    assert len(data["order"]) == 1
    assert data["order"][0]["modifiers"] == ["updated modifier", "extra sauce"]
    assert data["total"] == menu_items[1]["price"]

def test_delete_order():
    """Test deleting an order"""
    # First create an order
    menu_response = client.get("/api/menu")
    assert menu_response.status_code == 200
    menu_items = menu_response.json()
    
    order_data = {
        "order": [
            {
                "name": menu_items[0]["name"],
                "price": menu_items[0]["price"],
                "category": menu_items[0]["category"],
                "modifiers": ["to be deleted"]
            }
        ],
        "total": menu_items[0]["price"],
        "order_type": "delivery",
        "customer_name": "Delete Customer",
        "delivery_address": "Delete Address"
    }
    
    create_response = client.post("/api/orders", json=order_data)
    assert create_response.status_code == 200
    created_order = create_response.json()
    
    # Now delete the order
    response = client.delete(f"/api/orders/{created_order['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Order deleted successfully"
    
    # Verify the order is no longer retrievable
    get_response = client.get(f"/api/orders/{created_order['id']}")
    assert get_response.status_code == 404