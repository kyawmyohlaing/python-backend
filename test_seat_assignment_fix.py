#!/usr/bin/env python3
"""
Test script to verify the seat assignment fix in the backend.
This script tests the assign-seat and release-seat endpoints.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8088/api/tables"  # Adjust if your backend runs on a different port

def test_seat_assignment():
    """Test assigning and releasing seats"""
    print("Testing seat assignment fix...")
    
    # Test table ID (adjust as needed)
    table_id = 3  # Using table 3 as in the user's example
    seat_number = 2  # Using seat 2 as in the user's example
    customer_name = "kyawmy"  # Using the customer name from the user's example
    
    try:
        # First, get the current table status
        print(f"Getting current status of table {table_id}...")
        response = requests.get(f"{BASE_URL}/{table_id}")
        if response.status_code == 200:
            table_data = response.json()
            print(f"Current table status: {table_data['status']}")
            print(f"Seats: {table_data['seats']}")
        else:
            print(f"Failed to get table data: {response.status_code}")
            return
        
        # Assign a customer to seat 2
        print(f"\nAssigning customer '{customer_name}' to seat {seat_number} on table {table_id}...")
        assign_response = requests.post(
            f"{BASE_URL}/{table_id}/assign-seat/{seat_number}",
            data={"customer_name": customer_name}
        )
        
        if assign_response.status_code == 200:
            result = assign_response.json()
            print(f"Assignment successful: {result['message']}")
        else:
            print(f"Assignment failed: {assign_response.status_code} - {assign_response.text}")
            return
        
        # Get the updated table status
        print(f"\nGetting updated status of table {table_id}...")
        response = requests.get(f"{BASE_URL}/{table_id}")
        if response.status_code == 200:
            table_data = response.json()
            print(f"Updated table status: {table_data['status']}")
            print(f"Updated seats: {table_data['seats']}")
            
            # Check if the specific seat was updated correctly
            assigned_seat = next((seat for seat in table_data['seats'] if seat['seat_number'] == seat_number), None)
            if assigned_seat:
                if assigned_seat['status'] == 'occupied' and assigned_seat['customer_name'] == customer_name:
                    print(f"✓ Seat {seat_number} correctly assigned to {customer_name}")
                else:
                    print(f"✗ Seat {seat_number} not correctly assigned. Status: {assigned_seat['status']}, Customer: {assigned_seat['customer_name']}")
            else:
                print(f"✗ Seat {seat_number} not found in seats array")
        else:
            print(f"Failed to get updated table data: {response.status_code}")
        
        # Release the seat
        print(f"\nReleasing seat {seat_number} on table {table_id}...")
        release_response = requests.post(f"{BASE_URL}/{table_id}/release-seat/{seat_number}")
        
        if release_response.status_code == 200:
            result = release_response.json()
            print(f"Release successful: {result['message']}")
        else:
            print(f"Release failed: {release_response.status_code} - {release_response.text}")
            return
            
        # Get the final table status
        print(f"\nGetting final status of table {table_id}...")
        response = requests.get(f"{BASE_URL}/{table_id}")
        if response.status_code == 200:
            table_data = response.json()
            print(f"Final table status: {table_data['status']}")
            print(f"Final seats: {table_data['seats']}")
            
            # Check if the specific seat was released correctly
            released_seat = next((seat for seat in table_data['seats'] if seat['seat_number'] == seat_number), None)
            if released_seat:
                if released_seat['status'] == 'available' and released_seat['customer_name'] is None:
                    print(f"✓ Seat {seat_number} correctly released")
                else:
                    print(f"✗ Seat {seat_number} not correctly released. Status: {released_seat['status']}, Customer: {released_seat['customer_name']}")
            else:
                print(f"✗ Seat {seat_number} not found in seats array")
        else:
            print(f"Failed to get final table data: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend server. Make sure it's running.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    test_seat_assignment()