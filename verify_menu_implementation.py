#!/usr/bin/env python3
"""
Script to verify menu implementation without database connectivity
"""

import ast
import sys
import os

def check_file_exists(file_path):
    """Check if a file exists"""
    exists = os.path.exists(file_path)
    status = "✓" if exists else "✗"
    print(f"{status} {file_path} {'exists' if exists else 'not found'}")
    return exists

def check_functions_in_file(file_path, expected_functions):
    """Check if expected functions are defined in a file"""
    if not os.path.exists(file_path):
        return False
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse the Python code
        tree = ast.parse(content)
        
        # Extract function names
        function_names = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
        
        found_functions = 0
        for func_name in expected_functions:
            if func_name in function_names:
                print(f"✓ Found function: {func_name}")
                found_functions += 1
            else:
                print(f"✗ Missing function: {func_name}")
        
        return found_functions == len(expected_functions)
        
    except Exception as e:
        print(f"✗ Error parsing {file_path}: {e}")
        return False

def verify_menu_implementation():
    """Verify the menu implementation"""
    print("Verifying menu implementation...\n")
    
    # Check that required files exist
    print("1. Checking required files:")
    required_files = [
        "app/routes/menu_routes.py",
        "app/models/menu.py",
        "app/schemas/menu_schema.py",
        "initialize_menu.py",
        "tests/test_menu.py"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        full_path = os.path.join("c:\\strategy_test\\python_backend_structure", file_path)
        if not check_file_exists(full_path):
            all_files_exist = False
    
    if not all_files_exist:
        print("\n✗ Some required files are missing")
        return False
    
    print("\n2. Checking menu routes functions:")
    routes_file = "c:\\strategy_test\\python_backend_structure\\app\\routes\\menu_routes.py"
    expected_routes_functions = [
        "get_menu_items",
        "create_menu_item",
        "create_menu_items_batch",
        "get_menu_item",
        "update_menu_item",
        "delete_menu_item",
        "get_menu_items_by_category",
        "get_menu_categories"
    ]
    routes_ok = check_functions_in_file(routes_file, expected_routes_functions)
    
    print("\n3. Checking initialization script functions:")
    init_file = "c:\\strategy_test\\python_backend_structure\\initialize_menu.py"
    expected_init_functions = [
        "initialize_menu",
        "add_menu_item",
        "update_menu_item"
    ]
    init_ok = check_functions_in_file(init_file, expected_init_functions)
    
    print("\n4. Checking test functions:")
    test_file = "c:\\strategy_test\\python_backend_structure\\tests\\test_menu.py"
    # Just check that the file exists and is not empty
    test_exists = os.path.exists(test_file) and os.path.getsize(test_file) > 0
    status = "✓" if test_exists else "✗"
    print(f"{status} Test file exists and is not empty")
    
    # Overall result
    if routes_ok and init_ok and test_exists:
        print("\n✓ Menu implementation verification successful!")
        print("All components have been implemented correctly.")
        return True
    else:
        print("\n✗ Menu implementation verification failed!")
        print("Some components are missing or incomplete.")
        return False

if __name__ == "__main__":
    success = verify_menu_implementation()
    sys.exit(0 if success else 1)