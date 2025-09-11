#!/usr/bin/env python3
"""
Test script for physical printer connectivity
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_escpos_availability():
    """Test if escpos library is available"""
    try:
        from escpos.printer import Usb, Network
        print("✓ ESC/POS library is available")
        return True
    except ImportError as e:
        print(f"✗ ESC/POS library not available: {e}")
        print("  To install, run: pip install python-escpos")
        return False

def test_usb_printer_connection(vendor_id=0x04b8, product_id=0x0202):
    """Test USB printer connection"""
    try:
        from escpos.printer import Usb
        
        print(f"Testing USB printer connection (Vendor: 0x{vendor_id:04x}, Product: 0x{product_id:04x})")
        
        # Try to connect to the printer
        printer = Usb(vendor_id, product_id, 0, 0x81, 0x03)
        
        # Send a simple test
        printer.text("USB Printer Test Successful!\n")
        printer.text("This is a test from the KOT system.\n")
        printer.cut()
        printer.close()
        
        print("✓ USB printer connection successful")
        return True
        
    except Exception as e:
        print(f"✗ USB printer connection failed: {e}")
        return False

def test_network_printer_connection(ip_address="127.0.0.1", port=9100):
    """Test network printer connection"""
    try:
        from escpos.printer import Network
        
        print(f"Testing network printer connection ({ip_address}:{port})")
        
        # Try to connect to the printer
        printer = Network(ip_address, port)
        
        # Send a simple test
        printer.text("Network Printer Test Successful!\n")
        printer.text("This is a test from the KOT system.\n")
        printer.cut()
        printer.close()
        
        print("✓ Network printer connection successful")
        return True
        
    except Exception as e:
        print(f"✗ Network printer connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("Physical Printer Testing")
    print("=" * 30)
    
    # Test ESC/POS availability
    if not test_escpos_availability():
        print("\nCannot proceed with printer tests without ESC/POS library.")
        return
    
    print()
    
    # Ask user what type of printer to test
    print("Which type of printer would you like to test?")
    print("1. USB Printer")
    print("2. Network Printer")
    print("3. Both")
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            # Test USB printer
            vendor_id = input("Enter Vendor ID (hex, e.g., 0x04b8): ").strip()
            product_id = input("Enter Product ID (hex, e.g., 0x0202): ").strip()
            
            try:
                vendor_id = int(vendor_id, 16) if vendor_id.startswith("0x") else int(vendor_id)
                product_id = int(product_id, 16) if product_id.startswith("0x") else int(product_id)
                test_usb_printer_connection(vendor_id, product_id)
            except ValueError:
                print("Invalid vendor or product ID format.")
                
        elif choice == "2":
            # Test network printer
            ip_address = input("Enter printer IP address (default: 127.0.0.1): ").strip() or "127.0.0.1"
            port = input("Enter printer port (default: 9100): ").strip() or "9100"
            
            try:
                port = int(port)
                test_network_printer_connection(ip_address, port)
            except ValueError:
                print("Invalid port number.")
                
        elif choice == "3":
            # Test both
            print("Testing USB printer...")
            test_usb_printer_connection()
            
            print("\nTesting network printer...")
            test_network_printer_connection()
            
        else:
            print("Invalid choice.")
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()