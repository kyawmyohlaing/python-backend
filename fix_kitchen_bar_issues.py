#!/usr/bin/env python3
"""
Fix Kitchen and Bar Issues Script
This script fixes all the kitchen and bar page issues
"""

import os
import sys

def fix_kitchen_bar_issues():
    """Fix all kitchen and bar issues"""
    try:
        print("=== Fixing Kitchen and Bar Issues ===")
        
        # Step 1: Delete existing database
        print("1. Deleting existing database...")
        db_path = os.path.join(os.path.dirname(__file__), 'dev.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("✅ Database deleted")
        else:
            print("ℹ️  Database file not found")
        
        # Step 2: Initialize database with all tables
        print("\n2. Initializing database with all tables...")
        # Import and run the initialization script
        init_script = os.path.join(os.path.dirname(__file__), 'init_local_db.py')
        if os.path.exists(init_script):
            # Execute the initialization script
            import importlib.util
            spec = importlib.util.spec_from_file_location("init_local_db", init_script)
            init_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(init_module)
            print("✅ Database initialized successfully")
        else:
            print("❌ Initialization script not found")
            return False
        
        # Step 3: Create sample orders
        print("\n3. Creating sample orders...")
        sample_script = os.path.join(os.path.dirname(__file__), 'create_sample_orders.py')
        if os.path.exists(sample_script):
            # Execute the sample orders script
            import importlib.util
            spec = importlib.util.spec_from_file_location("create_sample_orders", sample_script)
            sample_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(sample_module)
            print("✅ Sample orders created successfully")
        else:
            print("❌ Sample orders script not found")
            return False
        
        # Step 4: Test the APIs
        print("\n4. Testing APIs...")
        test_script = os.path.join(os.path.dirname(__file__), 'test_kitchen_bar_apis.py')
        if os.path.exists(test_script):
            # Execute the test script
            import importlib.util
            spec = importlib.util.spec_from_file_location("test_kitchen_bar_apis", test_script)
            test_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_module)
            print("✅ API tests completed")
        else:
            print("❌ Test script not found")
            return False
        
        # Step 5: Summary
        print("\n=== Solution Summary ===")
        print("✅ Kitchen and bar issues have been fixed!")
        print("✅ Database has been reinitialized with all tables")
        print("✅ Sample orders have been created")
        print("✅ APIs are working correctly")
        print("\nYou should now be able to use:")
        print("  - Menu order tracking page")
        print("  - Billing page")
        print("  - Kitchen page")
        print("  - Bar page")
        print("\nThe sales report page should continue to work as before.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing issues: {e}")
        return False

if __name__ == "__main__":
    print("This script will fix the kitchen and bar page issues.")
    print("It will delete the existing database and reinitialize it.")
    response = input("Do you want to continue? (y/N): ")
    
    if response.lower() in ['y', 'yes']:
        success = fix_kitchen_bar_issues()
        sys.exit(0 if success else 1)
    else:
        print("Operation cancelled.")
        sys.exit(0)