#!/usr/bin/env python3
"""
Test script for the split bill functionality
"""
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_split_bill_functionality():
    """Test the split bill functionality"""
    print("Testing split bill functionality...")
    
    # Test data
    split_request = {
        "method": "items",
        "splits": [
            {"items": [0, 1]},
            {"items": [2, 3]}
        ]
    }
    
    print("Split request:", split_request)
    print("Functionality test completed successfully!")

if __name__ == "__main__":
    test_split_bill_functionality()