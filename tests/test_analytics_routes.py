"""
Test file for analytics routes
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_get_top_selling_items():
    """Test the get_top_selling_items endpoint"""
    response = client.get("/api/analytics/reports/top-items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    # Check that items is a list
    assert isinstance(data["items"], list)

def test_get_top_selling_items_with_limit():
    """Test the get_top_selling_items endpoint with limit parameter"""
    response = client.get("/api/analytics/reports/top-items?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    # Check that items is a list and has at most 5 items
    assert isinstance(data["items"], list)
    assert len(data["items"]) <= 5

def test_get_peak_hours():
    """Test the get_peak_hours endpoint"""
    response = client.get("/api/analytics/reports/peak-hours")
    assert response.status_code == 200
    data = response.json()
    assert "hours" in data
    # Check that hours is a list with 24 items (one for each hour)
    assert isinstance(data["hours"], list)
    assert len(data["hours"]) == 24

def test_get_daily_sales_report():
    """Test the get_daily_sales_report endpoint"""
    response = client.get("/api/analytics/reports/daily")
    assert response.status_code == 200
    data = response.json()
    assert "sales_data" in data
    assert "total_sales" in data
    assert "total_orders" in data
    assert "average_daily_sales" in data
    # Check that sales_data is a list
    assert isinstance(data["sales_data"], list)

def test_get_weekly_sales_report():
    """Test the get_weekly_sales_report endpoint"""
    response = client.get("/api/analytics/reports/weekly")
    assert response.status_code == 200
    data = response.json()
    assert "sales_data" in data
    assert "total_sales" in data
    assert "total_orders" in data
    assert "average_weekly_sales" in data
    # Check that sales_data is a list
    assert isinstance(data["sales_data"], list)

def test_get_monthly_sales_report():
    """Test the get_monthly_sales_report endpoint"""
    response = client.get("/api/analytics/reports/monthly")
    assert response.status_code == 200
    data = response.json()
    assert "sales_data" in data
    assert "total_sales" in data
    assert "total_orders" in data
    assert "average_monthly_sales" in data
    # Check that sales_data is a list
    assert isinstance(data["sales_data"], list)

def test_get_top_selling_items_with_date_range():
    """Test the get_top_selling_items endpoint with date range"""
    # Calculate date range (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    response = client.get(
        f"/api/analytics/reports/top-items?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_get_peak_hours_with_date_range():
    """Test the get_peak_hours endpoint with date range"""
    # Calculate date range (last 7 days)
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)
    
    response = client.get(
        f"/api/analytics/reports/peak-hours?start_date={start_date.isoformat()}&end_date={end_date.isoformat()}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "hours" in data
    assert isinstance(data["hours"], list)
    assert len(data["hours"]) == 24

def test_invalid_limit_parameter():
    """Test the get_top_selling_items endpoint with invalid limit parameter"""
    response = client.get("/api/analytics/reports/top-items?limit=0")
    # Should return 422 for validation error
    assert response.status_code == 422

def test_excessive_limit_parameter():
    """Test the get_top_selling_items endpoint with excessive limit parameter"""
    response = client.get("/api/analytics/reports/top-items?limit=101")
    # Should return 422 for validation error
    assert response.status_code == 422