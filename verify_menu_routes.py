#!/usr/bin/env python3
"""
Script to verify that menu routes can be imported and are correctly defined
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def verify_menu_routes():
    """Verify that menu routes are correctly defined"""
    print("Verifying menu routes...")
    
    try:
        # Import the menu router
        from routes.menu_routes import router
        print("✓ Menu router imported successfully")
        
        # Check that all expected routes are present
        expected_routes = [
            ('GET', '/'),
            ('POST', '/'),
            ('POST', '/batch'),
            ('GET', '/{item_id}'),
            ('PUT', '/{item_id}'),
            ('DELETE', '/{item_id}'),
            ('GET', '/category/{category}'),
            ('GET', '/categories')
        ]
        
        # Get all routes
        routes = []
        for route in router.routes:
            routes.append((route.methods, route.path))
        
        print(f"Found {len(routes)} routes:")
        for methods, path in routes:
            print(f"  {methods} {path}")
        
        # Check for expected routes
        found_routes = 0
        for expected_method, expected_path in expected_routes:
            for methods, path in routes:
                if expected_method in methods and expected_path == path:
                    print(f"✓ Found route: {expected_method} {expected_path}")
                    found_routes += 1
                    break
            else:
                print(f"✗ Missing route: {expected_method} {expected_path}")
        
        print(f"\nFound {found_routes}/{len(expected_routes)} expected routes")
        
        if found_routes == len(expected_routes):
            print("✓ All menu routes are correctly defined!")
            return True
        else:
            print("✗ Some menu routes are missing")
            return False
            
    except Exception as e:
        print(f"✗ Error verifying menu routes: {e}")
        return False

if __name__ == "__main__":
    success = verify_menu_routes()
    sys.exit(0 if success else 1)