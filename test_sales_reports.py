#!/usr/bin/env python3
"""
Test script for Sales Reports Feature
This script tests the daily/weekly/monthly sales reports functionality
in the FastAPI backend and React frontend integration.
"""

import requests
import json
from datetime import datetime, timedelta
import os

# Configuration
BASE_URL = "http://localhost:8000"  # FastAPI backend
FRONTEND_URL = "http://localhost:3000"  # React frontend

def test_backend_endpoints():
    """Test the backend API endpoints for sales reports"""
    print("Testing Backend Sales Reports Endpoints...")
    
    # Test authentication (assuming we need a token)
    print("1. Testing authentication...")
    try:
        # First, let's try to login or get a token
        # This would depend on your auth implementation
        print("   - Authentication endpoint test: SKIPPED (implementation-dependent)")
    except Exception as e:
        print(f"   - Authentication error: {e}")
    
    # Test daily sales report endpoint
    print("2. Testing daily sales report endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/reports/daily")
        print(f"   - Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Response: {json.dumps(data, indent=2)[:200]}...")
            print("   - Daily sales report endpoint: SUCCESS")
        else:
            print(f"   - Daily sales report endpoint: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"   - Daily sales report endpoint: ERROR - {e}")
    
    # Test weekly sales report endpoint
    print("3. Testing weekly sales report endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/reports/weekly")
        print(f"   - Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Response: {json.dumps(data, indent=2)[:200]}...")
            print("   - Weekly sales report endpoint: SUCCESS")
        else:
            print(f"   - Weekly sales report endpoint: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"   - Weekly sales report endpoint: ERROR - {e}")
    
    # Test monthly sales report endpoint
    print("4. Testing monthly sales report endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/reports/monthly")
        print(f"   - Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Response: {json.dumps(data, indent=2)[:200]}...")
            print("   - Monthly sales report endpoint: SUCCESS")
        else:
            print(f"   - Monthly sales report endpoint: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"   - Monthly sales report endpoint: ERROR - {e}")
    
    # Test with date filters
    print("5. Testing sales reports with date filters...")
    try:
        # Calculate date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        
        response = requests.get(f"{BASE_URL}/api/analytics/reports/daily", params=params)
        print(f"   - Daily with filters - Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   - Daily sales report with filters: SUCCESS")
        else:
            print(f"   - Daily sales report with filters: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"   - Sales reports with date filters: ERROR - {e}")

def test_frontend_integration():
    """Test the frontend integration with the backend"""
    print("\nTesting Frontend Integration...")
    
    # Test if frontend is accessible
    print("1. Testing frontend accessibility...")
    try:
        response = requests.get(FRONTEND_URL)
        print(f"   - Frontend Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   - Frontend accessibility: SUCCESS")
        else:
            print(f"   - Frontend accessibility: FAILED (Status {response.status_code})")
    except Exception as e:
        print(f"   - Frontend accessibility: ERROR - {e}")
    
    # Test if API service functions exist (this would require checking the built frontend)
    print("2. Testing API service functions...")
    print("   - API service function testing: MANUAL VERIFICATION REQUIRED")
    print("   - Check that fetchDailySalesReport, fetchWeeklySalesReport, and fetchMonthlySalesReport functions exist")

def test_data_consistency():
    """Test data consistency between different report types"""
    print("\nTesting Data Consistency...")
    
    print("1. Comparing report data...")
    print("   - Data consistency testing: MANUAL VERIFICATION REQUIRED")
    print("   - Verify that daily, weekly, and monthly reports show consistent data")

def main():
    """Main test function"""
    print("Sales Reports Feature Test Suite")
    print("=" * 50)
    
    # Test backend endpoints
    test_backend_endpoints()
    
    # Test frontend integration
    test_frontend_integration()
    
    # Test data consistency
    test_data_consistency()
    
    print("\n" + "=" * 50)
    print("Test suite completed. Please verify the results above.")
    print("Note: Some tests may require manual verification or a running backend/frontend.")

if __name__ == "__main__":
    main()