#!/usr/bin/env python3
"""
Simple test script to verify Table & Seat Management API endpoints work correctly
"""
import sys
import os

# Add the app directory to the path so we can import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_table_api_endpoints():
    """Test that table API endpoints are properly defined"""
    try:
        # Mock the database dependency to avoid connection issues
        import app.database
        import app.dependencies
        
        # Save original Base
        original_base = app.database.Base
        
        # Create a mock Base class with metadata
        class MockBase:
            def __init__(self):
                self.metadata = MockMetadata()
        
        class MockMetadata:
            def __init__(self):
                pass
            
            def create_all(self, bind):
                pass  # No-op
        
        # Replace Base with mock
        app.database.Base = MockBase()
        app.dependencies.get_db = lambda: None
        
        # Mock the database creation
        import app.main
        # Save original Base
        original_main_base = app.main.Base
        # Replace with mock
        app.main.Base = MockBase()
        
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test that the API endpoints exist by checking the app routes
        routes = [route.path for route in app.routes]
        
        # Check for table management routes
        expected_routes = [
            "/api/tables/",
            "/api/tables/{table_id}",
            "/api/tables/{table_id}/assign/{order_id}",
            "/api/tables/{table_id}/release",
            "/api/tables/{table_id}/assign-seat/{seat_number}",
            "/api/tables/{table_id}/release-seat/{seat_number}",
            "/api/tables/merge-tables/{table_id_1}/{table_id_2}",
            "/api/tables/split-bill/{table_id}",
            "/api/tables/occupied/",
            "/api/tables/available/"
        ]
        
        missing_routes = []
        for route in expected_routes:
            # Handle route parameter formatting
            route_found = False
            for app_route in routes:
                # Simple pattern matching for routes with parameters
                if route.replace('{table_id}', '1').replace('{order_id}', '1').replace('{seat_number}', '1').replace('{table_id_1}', '1').replace('{table_id_2}', '2') in app_route:
                    route_found = True
                    break
                if route == app_route:
                    route_found = True
                    break
            
            if not route_found:
                missing_routes.append(route)
        
        if missing_routes:
            print("X Missing API routes:")
            for route in missing_routes:
                print(f"  - {route}")
            print("\nAll defined routes:")
            for route in sorted(routes):
                print(f"  - {route}")
            return False
        else:
            print("All table management API routes are defined")
            return True
            
    except Exception as e:
        print(f"X Error testing API endpoints: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Table & Seat Management API Endpoints...")
    print("=" * 50)
    
    success = test_table_api_endpoints()
    
    if success:
        print("\nAll API endpoint tests passed!")
    else:
        print("\nSome API endpoint tests failed!")
    
    sys.exit(0 if success else 1)