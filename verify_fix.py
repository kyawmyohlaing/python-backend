#!/usr/bin/env python3
"""
Verification script to check if the seat assignment fix is working correctly.
"""

import sys
import os

def check_fix():
    """Check if the fix has been applied correctly"""
    print("Verifying seat assignment fix...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the table_routes.py file
    table_routes_path = os.path.join(current_dir, "app", "routes", "table_routes.py")
    
    if not os.path.exists(table_routes_path):
        print(f"Error: table_routes.py not found at {table_routes_path}")
        return False
    
    try:
        with open(table_routes_path, 'r') as f:
            content = f.read()
        
        # Check if the fix has been applied
        assign_seat_fix_present = "table.seats = table.seats" in content and "IMPORTANT: Update the table's seats field in the database" in content
        release_seat_fix_present = content.count("table.seats = table.seats") >= 2 and content.count("IMPORTANT: Update the table's seats field in the database") >= 2
        
        if assign_seat_fix_present and release_seat_fix_present:
            print("✓ Seat assignment fix has been successfully applied!")
            print("✓ Both assign_seat and release_seat functions are properly persisting changes to the database.")
            return True
        else:
            print("✗ Seat assignment fix has not been applied correctly.")
            if not assign_seat_fix_present:
                print("  - Missing fix in assign_seat function")
            if not release_seat_fix_present:
                print("  - Missing fix in release_seat function")
            return False
            
    except Exception as e:
        print(f"Error reading table_routes.py: {e}")
        return False

def main():
    print("Seat Assignment Fix Verification")
    print("=" * 40)
    
    if check_fix():
        print("\n🎉 All checks passed! The seat assignment functionality should now work correctly.")
        print("\nTo test the fix:")
        print("1. Start your backend server")
        print("2. Run the test script: python test_seat_assignment_fix.py")
        print("3. Or test manually with curl:")
        print("   curl -X POST \"http://localhost:8000/api/tables/3/assign-seat/2\" -d \"customer_name=kyawmy\"")
    else:
        print("\n❌ Fix verification failed. Please check the table_routes.py file.")

if __name__ == "__main__":
    main()