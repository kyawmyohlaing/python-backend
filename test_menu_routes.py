#!/usr/bin/env python3
"""
Test script to verify menu routes are correctly ordered
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_route_ordering():
    """Test that routes are correctly ordered to avoid conflicts"""
    try:
        # Import the router
        from routes.menu_routes import router
        
        # Get all routes
        routes = []
        for route in router.routes:
            routes.append((route.methods, route.path))
        
        print("Menu routes in order:")
        for i, (methods, path) in enumerate(routes):
            print(f"{i+1}. {methods} {path}")
        
        # Check that /categories comes before /{item_id}
        categories_index = None
        item_id_index = None
        
        for i, (methods, path) in enumerate(routes):
            if 'GET' in methods and path == '/categories':
                categories_index = i
            elif 'GET' in methods and path == '/{item_id}':
                item_id_index = i
        
        if categories_index is not None and item_id_index is not None:
            if categories_index < item_id_index:
                print("\n✓ Route ordering is correct: /categories comes before /{item_id}")
                return True
            else:
                print(f"\n✗ Route ordering is incorrect: /categories (index {categories_index}) comes after /{{item_id}} (index {item_id_index})")
                return False
        else:
            print("\n? Could not find expected routes")
            return False
            
    except Exception as e:
        print(f"Error testing route ordering: {e}")
        return False

if __name__ == "__main__":
    success = test_route_ordering()
    sys.exit(0 if success else 1)