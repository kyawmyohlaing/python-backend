import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.order import Order
from app.models.invoice import Invoice
import json

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop the tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_order():
    """Create a sample order for testing"""
    order_data = [
        {"name": "Burger", "price": 12.00, "category": "Main Course"},
        {"name": "Fries", "price": 5.00, "category": "Sides"},
        {"name": "Soda", "price": 3.50, "category": "Drinks"}
    ]
    
    db = TestingSessionLocal()
    order = Order(
        total=20.50,
        order_data=json.dumps(order_data),
        order_type="dine-in",
        table_number="5",
        customer_name="John Doe",
        customer_phone="123-456-7890"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    db.close()
    
    return order

def test_create_invoice_from_order(setup_database, sample_order):
    """Test creating an invoice from an order"""
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00},
            {"name": "Fries", "category": "Sides", "price": 5.00},
            {"name": "Soda", "category": "Drinks", "price": 3.50}
        ]
    }
    
    response = client.post("/api/invoices/", json=invoice_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["order_id"] == sample_order.id
    assert data["invoice_number"].startswith("INV-")
    assert data["customer_name"] == "John Doe"
    assert data["total"] == 20.50

def test_get_invoices(setup_database, sample_order):
    """Test getting all invoices"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    client.post("/api/invoices/", json=invoice_data)
    
    # Now get all invoices
    response = client.get("/api/invoices/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["order_id"] == sample_order.id

def test_get_invoice_by_id(setup_database, sample_order):
    """Test getting a specific invoice by ID"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    create_response = client.post("/api/invoices/", json=invoice_data)
    invoice_id = create_response.json()["id"]
    
    # Now get the invoice by ID
    response = client.get(f"/api/invoices/{invoice_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == invoice_id
    assert data["order_id"] == sample_order.id

def test_get_invoice_by_order_id(setup_database, sample_order):
    """Test getting an invoice by order ID"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    client.post("/api/invoices/", json=invoice_data)
    
    # Now get the invoice by order ID
    response = client.get(f"/api/invoices/order/{sample_order.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["order_id"] == sample_order.id

def test_update_invoice(setup_database, sample_order):
    """Test updating an invoice"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    create_response = client.post("/api/invoices/", json=invoice_data)
    invoice_id = create_response.json()["id"]
    
    # Now update the invoice
    update_data = {
        "customer_name": "Jane Smith",
        "total": 25.00
    }
    
    response = client.put(f"/api/invoices/{invoice_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "Jane Smith"
    assert data["total"] == 25.00

def test_delete_invoice(setup_database, sample_order):
    """Test deleting an invoice"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    create_response = client.post("/api/invoices/", json=invoice_data)
    invoice_id = create_response.json()["id"]
    
    # Now delete the invoice
    response = client.delete(f"/api/invoices/{invoice_id}")
    assert response.status_code == 200
    
    # Try to get the deleted invoice
    response = client.get(f"/api/invoices/{invoice_id}")
    assert response.status_code == 404

def test_create_invoice_for_nonexistent_order(setup_database):
    """Test creating an invoice for a non-existent order"""
    invoice_data = {
        "order_id": 99999,  # Non-existent order ID
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    response = client.post("/api/invoices/", json=invoice_data)
    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]

def test_create_duplicate_invoice(setup_database, sample_order):
    """Test creating a duplicate invoice for the same order"""
    # First create an invoice
    invoice_data = {
        "order_id": sample_order.id,
        "customer_name": "John Doe",
        "customer_phone": "123-456-7890",
        "order_type": "dine-in",
        "table_number": "5",
        "subtotal": 20.50,
        "total": 20.50,
        "invoice_items": [
            {"name": "Burger", "category": "Main Course", "price": 12.00}
        ]
    }
    
    # Create first invoice
    client.post("/api/invoices/", json=invoice_data)
    
    # Try to create duplicate invoice
    response = client.post("/api/invoices/", json=invoice_data)
    assert response.status_code == 400
    assert "Invoice already exists for this order" in response.json()["detail"]