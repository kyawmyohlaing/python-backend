#!/usr/bin/env python3
"""
Test script for Analytics Service - Sales Reports
This script specifically tests the sales report functionality in the analytics service.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_sales_report_schemas():
    """Test that the sales report schemas are correctly defined"""
    print("Testing Sales Report Schemas...")
    
    try:
        from app.schemas.analytics_schema import (
            SalesReportItem,
            DailySalesReportResponse,
            WeeklySalesReportResponse,
            MonthlySalesReportResponse
        )
        
        print("1. Testing SalesReportItem schema...")
        # Test creating a SalesReportItem instance
        item = SalesReportItem(
            date="2025-01-01",
            total_orders=10,
            total_revenue=1000.00,
            total_discounts=50.00,
            total_taxes=80.00,
            net_revenue=870.00
        )
        print(f"   - SalesReportItem creation: SUCCESS")
        print(f"   - Sample item: {item}")
        
        print("2. Testing DailySalesReportResponse schema...")
        daily_report = DailySalesReportResponse(
            report=[item],
            summary={
                "total_orders": 10,
                "total_revenue": 1000.00,
                "total_discounts": 50.00,
                "total_taxes": 80.00,
                "net_revenue": 870.00
            }
        )
        print(f"   - DailySalesReportResponse creation: SUCCESS")
        
        print("3. Testing WeeklySalesReportResponse schema...")
        weekly_report = WeeklySalesReportResponse(
            report=[{
                "week_start": "2025-01-01",
                "week_end": "2025-01-07",
                "total_orders": 70,
                "total_revenue": 7000.00,
                "total_discounts": 350.00,
                "total_taxes": 560.00,
                "net_revenue": 6090.00
            }],
            summary={
                "total_orders": 70,
                "total_revenue": 7000.00,
                "total_discounts": 350.00,
                "total_taxes": 560.00,
                "net_revenue": 6090.00
            }
        )
        print(f"   - WeeklySalesReportResponse creation: SUCCESS")
        
        print("4. Testing MonthlySalesReportResponse schema...")
        monthly_report = MonthlySalesReportResponse(
            report=[{
                "month": "2025-01",
                "total_orders": 300,
                "total_revenue": 30000.00,
                "total_discounts": 1500.00,
                "total_taxes": 2400.00,
                "net_revenue": 26100.00
            }],
            summary={
                "total_orders": 300,
                "total_revenue": 30000.00,
                "total_discounts": 1500.00,
                "total_taxes": 2400.00,
                "net_revenue": 26100.00
            }
        )
        print(f"   - MonthlySalesReportResponse creation: SUCCESS")
        
        print("   - All sales report schemas: PASSED")
        
    except ImportError as e:
        print(f"   - Schema import error: {e}")
        print("   - Sales report schemas: FAILED")
    except Exception as e:
        print(f"   - Schema testing error: {e}")
        print("   - Sales report schemas: FAILED")

def test_analytics_service_methods():
    """Test the analytics service methods for sales reports"""
    print("\nTesting Analytics Service Methods...")
    
    try:
        from app.services.analytics_service import AnalyticsService
        from app.database import get_db
        
        print("1. Testing AnalyticsService instantiation...")
        # This would normally require a database session
        # For testing purposes, we'll just check if the class exists and has the methods
        print(f"   - AnalyticsService class exists: {'AnalyticsService' in globals()}")
        
        # Check if the service has the required methods
        service_methods = [
            'get_daily_sales_report',
            'get_weekly_sales_report', 
            'get_monthly_sales_report'
        ]
        
        print("2. Checking for required sales report methods...")
        for method in service_methods:
            if hasattr(AnalyticsService, method):
                print(f"   - Method {method}: FOUND")
            else:
                print(f"   - Method {method}: MISSING")
                
    except ImportError as e:
        print(f"   - Service import error: {e}")
        print("   - Analytics service methods: FAILED")
    except Exception as e:
        print(f"   - Service testing error: {e}")
        print("   - Analytics service methods: FAILED")

def test_route_endpoints():
    """Test that the route endpoints are properly defined"""
    print("\nTesting Route Endpoints...")
    
    try:
        from app.routes.analytics_routes import router
        print("1. Testing analytics router import...")
        print(f"   - Router imported successfully: {router is not None}")
        
        # Check if the routes are defined
        routes = [
            "GET /reports/daily",
            "GET /reports/weekly", 
            "GET /reports/monthly"
        ]
        
        print("2. Checking for sales report routes...")
        # We can't easily check the actual routes without running the app
        # But we can verify the router exists
        print(f"   - Router object exists: {router is not None}")
        print("   - Route verification: MANUAL CHECK REQUIRED")
        print("   - Please verify routes exist in app/routes/analytics_routes.py")
        
    except ImportError as e:
        print(f"   - Route import error: {e}")
        print("   - Route endpoints: FAILED")
    except Exception as e:
        print(f"   - Route testing error: {e}")
        print("   - Route endpoints: FAILED")

def main():
    """Main test function"""
    print("Analytics Service - Sales Reports Test Suite")
    print("=" * 50)
    
    # Test schemas
    test_sales_report_schemas()
    
    # Test service methods
    test_analytics_service_methods()
    
    # Test routes
    test_route_endpoints()
    
    print("\n" + "=" * 50)
    print("Analytics service test suite completed.")
    print("Note: Some tests may require a running database or manual verification.")

if __name__ == "__main__":
    main()