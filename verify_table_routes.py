#!/usr/bin/env python3
"""
Simple script to verify Table & Seat Management route definitions
"""
import sys
import os
import ast

def check_table_routes():
    """Check that table routes are properly defined in the routes file"""
    try:
        # Read the table routes file
        routes_file = os.path.join(os.path.dirname(__file__), 'app', 'routes', 'table_routes.py')
        
        with open(routes_file, 'r') as f:
            content = f.read()
        
        # Parse the Python code
        tree = ast.parse(content)
        
        # Look for route decorators
        route_decorators = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ['get', 'post', 'put', 'delete'] and 'router' in ast.unparse(node.func.value):
                    # Extract the route path
                    if node.args:
                        path_arg = node.args[0]
                        if isinstance(path_arg, ast.Constant):
                            route_path = path_arg.value
                            route_decorators.append({
                                'method': node.func.attr,
                                'path': route_path
                            })
        
        # Expected table routes
        expected_routes = [
            {'method': 'get', 'path': '/'},
            {'method': 'get', 'path': '/{table_id}'},
            {'method': 'post', 'path': '/'},
            {'method': 'put', 'path': '/{table_id}'},
            {'method': 'delete', 'path': '/{table_id}'},
            {'method': 'post', 'path': '/{table_id}/assign/{order_id}'},
            {'method': 'post', 'path': '/{table_id}/release'},
            {'method': 'post', 'path': '/{table_id}/assign-seat/{seat_number}'},
            {'method': 'post', 'path': '/{table_id}/release-seat/{seat_number}'},
            {'method': 'post', 'path': '/merge-tables/{table_id_1}/{table_id_2}'},
            {'method': 'post', 'path': '/split-bill/{table_id}'},
            {'method': 'get', 'path': '/occupied/'},
            {'method': 'get', 'path': '/available/'}
        ]
        
        # Check if all expected routes are defined
        missing_routes = []
        for expected in expected_routes:
            found = False
            for route in route_decorators:
                if route['method'] == expected['method'] and route['path'] == expected['path']:
                    found = True
                    break
            if not found:
                missing_routes.append(expected)
        
        if missing_routes:
            print("❌ Missing table routes:")
            for route in missing_routes:
                print(f"  - {route['method'].upper()} {route['path']}")
            return False
        else:
            print("✅ All table management routes are defined:")
            for route in route_decorators:
                print(f"  - {route['method'].upper()} {route['path']}")
            return True
            
    except Exception as e:
        print(f"❌ Error checking table routes: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Verifying Table & Seat Management Route Definitions...")
    print("=" * 55)
    
    success = check_table_routes()
    
    if success:
        print("\n✅ All route definitions are correct!")
    else:
        print("\n❌ Some route definitions are missing!")
    
    sys.exit(0 if success else 1)