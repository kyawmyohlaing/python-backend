#!/usr/bin/env python3
"""
Test runner for Table & Seat Management API tests
"""
import subprocess
import sys
import os

def run_table_tests():
    """Run the table management tests"""
    print("Running Table & Seat Management API Tests...")
    print("=" * 50)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the endpoint tests directly with Python
    try:
        result = subprocess.run([
            "python", "test_table_api_endpoints.py"
        ], check=True, capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print("All table management tests passed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print("Table management tests failed!")
        print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False
    except FileNotFoundError:
        print("Error: test_table_api_endpoints.py not found.")
        return False

if __name__ == "__main__":
    success = run_table_tests()
    sys.exit(0 if success else 1)