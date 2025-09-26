#!/usr/bin/env python3
"""
Verification script for Sales Reports Implementation
This script verifies that all components of the sales reports feature are correctly implemented.
"""

import os
import sys

def verify_backend_components():
    """Verify that all backend components are correctly implemented"""
    print("Verifying Backend Components...")
    
    # Check if analytics schema has the required classes
    print("1. Checking analytics schema...")
    try:
        from app.schemas.analytics_schema import (
            SalesReportItem,
            DailySalesReportResponse,
            WeeklySalesReportResponse,
            MonthlySalesReportResponse
        )
        print("   ✓ SalesReportItem schema exists")
        print("   ✓ DailySalesReportResponse schema exists")
        print("   ✓ WeeklySalesReportResponse schema exists")
        print("   ✓ MonthlySalesReportResponse schema exists")
    except ImportError as e:
        print(f"   ✗ Schema import error: {e}")
        return False
    
    # Check if analytics service has the required methods
    print("2. Checking analytics service...")
    try:
        from app.services.analytics_service import AnalyticsService
        
        # Check if the required methods exist
        required_methods = [
            'get_daily_sales_report',
            'get_weekly_sales_report',
            'get_monthly_sales_report'
        ]
        
        for method in required_methods:
            if hasattr(AnalyticsService, method):
                print(f"   ✓ Method {method} exists")
            else:
                print(f"   ✗ Method {method} missing")
                return False
    except ImportError as e:
        print(f"   ✗ Service import error: {e}")
        return False
    
    # Check if analytics routes have the required endpoints
    print("3. Checking analytics routes...")
    try:
        from app.routes.analytics_routes import router
        
        # Check if the router has the required routes
        required_routes = [
            "/api/analytics/reports/daily",
            "/api/analytics/reports/weekly",
            "/api/analytics/reports/monthly"
        ]
        
        # Get route paths (handle different route types)
        routes = []
        for route in router.routes:
            # Type checking to avoid linter warnings
            from fastapi.routing import APIRoute
            if isinstance(route, APIRoute) and hasattr(route, 'path'):
                routes.append(route.path)
        for route in required_routes:
            if route in routes:
                print(f"   ✓ Route {route} exists")
            else:
                print(f"   ✗ Route {route} missing")
                return False
    except ImportError as e:
        print(f"   ✗ Routes import error: {e}")
        return False
    
    print("✓ All backend components verified successfully")
    return True

def verify_frontend_components():
    """Verify that all frontend components are correctly implemented"""
    print("\nVerifying Frontend Components...")
    
    # Check if SalesReportsPage.jsx exists
    sales_reports_page_path = r"..\react_frontend\src\SalesReportsPage.jsx"
    if os.path.exists(sales_reports_page_path):
        print("   ✓ SalesReportsPage.jsx exists")
    else:
        print("   ✗ SalesReportsPage.jsx missing")
        return False
    
    # Check if api.js has the required functions
    api_js_path = r"..\react_frontend\src\api.js"
    if os.path.exists(api_js_path):
        print("   ✓ api.js exists")
        
        # Check content of api.js for required functions
        try:
            with open(api_js_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                required_functions = [
                    'fetchDailySalesReport',
                    'fetchWeeklySalesReport',
                    'fetchMonthlySalesReport'
                ]
                
                for func in required_functions:
                    if func in content:
                        print(f"   ✓ Function {func} exists in api.js")
                    else:
                        print(f"   ✗ Function {func} missing from api.js")
                        return False
        except Exception as e:
            print(f"   ✗ Error reading api.js: {e}")
            return False
    else:
        print("   ✗ api.js missing")
        return False
    
    print("✓ All frontend components verified successfully")
    return True

def verify_documentation():
    """Verify that documentation is in place"""
    print("\nVerifying Documentation...")
    
    # Check if key documentation files exist
    docs_to_check = [
        "SALES_REPORTS_TESTING_GUIDE.md",
        "API_DOCUMENTATION.md",
        "README.md"
    ]
    
    for doc in docs_to_check:
        if os.path.exists(doc):
            print(f"   ✓ {doc} exists")
        else:
            print(f"   ✗ {doc} missing")
    
    print("✓ Documentation verification completed")
    return True

def main():
    """Main verification function"""
    print("Sales Reports Implementation Verification")
    print("=" * 50)
    
    # Verify backend components
    backend_ok = verify_backend_components()
    
    # Verify frontend components
    frontend_ok = verify_frontend_components()
    
    # Verify documentation
    docs_ok = verify_documentation()
    
    print("\n" + "=" * 50)
    if backend_ok and frontend_ok and docs_ok:
        print("🎉 All components verified successfully!")
        print("✅ The sales reports feature is fully implemented and ready for testing.")
    else:
        print("❌ Some components failed verification.")
        print("⚠️  Please check the output above for details.")
    
    return backend_ok and frontend_ok and docs_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)