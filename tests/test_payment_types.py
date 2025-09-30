import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models.order import Order, PaymentType
from sqlalchemy.orm import Session
from tests.conftest import override_get_db

# Override the database dependency for testing
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_order_with_payment_type():
    """Test creating an order with different payment types"""
    # Test with cash payment
    order_data = {
        "order": [
            {
                "name": "Burger",
                "price": 8.99,
                "category": "Main Course",
                "modifiers": ["extra cheese"]
            }
        ],
        "total": 8.99,
        "payment_type": "cash"
    }
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_type"] == "cash"
    
    # Test with card payment
    order_data["payment_type"] = "card"
    order_data["total"] = 12.99
    order_data["order"][0]["price"] = 12.99
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_type"] == "card"
    
    # Test with QR payment
    order_data["payment_type"] = "qr"
    order_data["total"] = 15.99
    order_data["order"][0]["price"] = 15.99
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_type"] == "qr"

def test_update_order_payment_type():
    """Test updating an order's payment type"""
    # Create an order first
    order_data = {
        "order": [
            {
                "name": "Pizza",
                "price": 12.99,
                "category": "Main Course"
            }
        ],
        "total": 12.99,
        "payment_type": "cash"
    }
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    created_order = response.json()
    order_id = created_order["id"]
    
    # Update the payment type
    update_data = {
        "payment_type": "card"
    }
    
    response = client.put(f"/api/orders/{order_id}", json=update_data)
    assert response.status_code == 200
    updated_order = response.json()
    assert updated_order["payment_type"] == "card"

def test_invalid_payment_type_defaults_to_cash():
    """Test that invalid payment types default to cash"""
    order_data = {
        "order": [
            {
                "name": "Salad",
                "price": 7.99,
                "category": "Appetizer"
            }
        ],
        "total": 7.99,
        "payment_type": "invalid_type"
    }
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    data = response.json()
    # Should default to cash for invalid payment types
    assert data["payment_type"] == "cash"

def test_create_invoice_with_payment_type():
    """Test that invoices inherit payment type from orders"""
    # Create an order with card payment
    order_data = {
        "order": [
            {
                "name": "Pasta",
                "price": 14.99,
                "category": "Main Course"
            }
        ],
        "total": 14.99,
        "payment_type": "card",
        "customer_name": "John Doe"
    }
    
    response = client.post("/api/orders/", json=order_data)
    assert response.status_code == 200
    created_order = response.json()
    order_id = created_order["id"]
    
    # Create an invoice from the order
    invoice_data = {
        "order_id": order_id,
        "customer_name": "John Doe",
        "order_type": "dine_in",
        "subtotal": 14.99,
        "total": 14.99,
        "invoice_items": [
            {
                "name": "Pasta",
                "category": "Main Course",
                "price": 14.99,
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/api/invoices/", json=invoice_data)
    assert response.status_code == 200
    invoice = response.json()
    # The invoice should inherit the payment type from the order
    assert invoice["payment_type"] == "card"