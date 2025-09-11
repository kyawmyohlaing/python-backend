# Physical Printer Testing Guide

## Overview

This guide explains how to test the KOT system with physical printers. The system supports various types of thermal printers commonly used in restaurant environments.

## Prerequisites

1. A compatible thermal printer (USB or network)
2. Required Python libraries installed
3. Proper printer drivers installed on your system

## Installing Required Dependencies

To test with physical printers, you'll need to install the `python-escpos` library:

```bash
pip install python-escpos
```

For USB printers, you may also need:
```bash
pip install pyusb
```

## Supported Printer Types

1. **USB Thermal Printers** - Most common for POS systems
2. **Network Thermal Printers** - For network-connected printing
3. **Bluetooth Printers** - For wireless printing solutions

## Testing with USB Printers

### Step 1: Identify Your Printer

First, identify your USB printer's vendor and product IDs:

```bash
# On Linux/Mac
lsusb

# On Windows, use Device Manager to find the USB device
```

### Step 2: Configure the Printer

Update the printer configuration in [app/services/kot_service.py](file:///c:/strategy_test/python_backend_structure/app/services/kot_service.py):

```python
self.printers = {
    "main_kitchen": {
        "type": "printer", 
        "location": "Main Kitchen", 
        "enabled": True, 
        "connection": "USB",
        "vendor_id": 0x04b8,      # Replace with your printer's vendor ID
        "product_id": 0x0202,     # Replace with your printer's product ID
        "timeout": 0
    }
}
```

### Step 3: Test the Connection

Create a test script to verify printer connectivity:

```python
# printer_test.py
from escpos.printer import Usb

# Replace with your actual vendor and product IDs
VENDOR_ID = 0x04b8
PRODUCT_ID = 0x0202

try:
    # Connect to the printer
    printer = Usb(VENDOR_ID, PRODUCT_ID, 0, 0x81, 0x03)
    
    # Print a test message
    printer.text("Printer Test Successful!\n")
    printer.text("This is a test of the KOT system.\n")
    printer.cut()
    
    # Close the connection
    printer.close()
    
    print("Printer test completed successfully!")
    
except Exception as e:
    print(f"Printer test failed: {e}")
```

## Testing with Network Printers

### Step 1: Configure the Printer

Update the printer configuration in [app/services/kot_service.py](file:///c:/strategy_test/python_backend_structure/app/services/kot_service.py):

```python
self.printers = {
    "main_kitchen": {
        "type": "printer", 
        "location": "Main Kitchen", 
        "enabled": True, 
        "connection": "network",
        "ip_address": "192.168.1.100",  # Replace with your printer's IP
        "port": 9100
    }
}
```

### Step 2: Test the Connection

Create a test script for network printers:

```python
# network_printer_test.py
from escpos.printer import Network

# Replace with your actual printer IP and port
PRINTER_IP = "192.168.1.100"
PRINTER_PORT = 9100

try:
    # Connect to the network printer
    printer = Network(PRINTER_IP, PRINTER_PORT)
    
    # Print a test message
    printer.text("Network Printer Test Successful!\n")
    printer.text("This is a test of the KOT system.\n")
    printer.cut()
    
    # Close the connection
    printer.close()
    
    print("Network printer test completed successfully!")
    
except Exception as e:
    print(f"Network printer test failed: {e}")
```

## Testing with the KOT System

### Step 1: Update the KOT Service

Modify the [_send_to_physical_printer](file:///c:/strategy_test/python_backend_structure/app/services/kot_service.py#L121-L161) method in [app/services/kot_service.py](file:///c:/strategy_test/python_backend_structure/app/services/kot_service.py) to support actual printer communication:

```python
def _send_to_physical_printer(self, kitchen_order: KitchenOrderDetail, printer_id: str, kot_content: str) -> Dict[str, any]:
    """
    Send KOT to a physical printer
    """
    try:
        printer_info = self.printers[printer_id]
        
        # Handle USB printer
        if printer_info.get("connection") == "USB":
            from escpos.printer import Usb
            
            # Get printer identifiers
            vendor_id = printer_info.get("vendor_id", 0x04b8)
            product_id = printer_info.get("product_id", 0x0202)
            timeout = printer_info.get("timeout", 0)
            in_ep = printer_info.get("in_ep", 0x81)
            out_ep = printer_info.get("out_ep", 0x03)
            
            # Connect to printer
            printer = Usb(vendor_id, product_id, timeout, in_ep, out_ep)
            
            # Print content
            printer.text(kot_content)
            printer.cut()
            
            # Close connection
            printer.close()
            
            logger.info(f"[KOT SERVICE] Printed to USB printer {printer_id}")
            return {"success": True, "message": f"KOT sent to USB printer {printer_id}", "content": kot_content}
        
        # Handle network printer
        elif printer_info.get("connection") == "network":
            from escpos.printer import Network
            
            # Get network details
            ip_address = printer_info.get("ip_address", "127.0.0.1")
            port = printer_info.get("port", 9100)
            
            # Connect to network printer
            printer = Network(ip_address, port)
            
            # Print content
            printer.text(kot_content)
            printer.cut()
            
            # Close connection
            printer.close()
            
            logger.info(f"[KOT SERVICE] Printed to network printer {printer_id}")
            return {"success": True, "message": f"KOT sent to network printer {printer_id}", "content": kot_content}
        
        # Fallback to simulation if connection type not supported
        else:
            logger.info(f"[KOT SERVICE] Simulating print to {printer_id} ({printer_info['location']})")
            logger.info(kot_content)
            return {"success": True, "message": f"Simulated print to {printer_id}", "content": kot_content}
            
    except Exception as e:
        error_msg = f"[KOT SERVICE] Error sending to physical printer {printer_id}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "message": error_msg}
```

### Step 2: Run a Full Test

Use the existing test script to verify the full KOT workflow:

```bash
python test_api.py
```

## Troubleshooting Common Issues

### 1. Permission Errors (Linux/Mac)

If you get permission errors with USB printers:

```bash
# Add your user to the dialout group (Ubuntu/Debian)
sudo usermod -a -G dialout $USER

# Or create a udev rule for the printer
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0666"' | sudo tee /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 2. Library Import Errors

If you get import errors:

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get install libusb-1.0-0-dev libudev-dev

# Reinstall the Python packages
pip uninstall python-escpos pyusb
pip install python-escpos pyusb
```

### 3. Printer Not Found

If the printer isn't detected:
1. Verify the vendor and product IDs are correct
2. Check that the printer is properly connected
3. Ensure the printer is powered on
4. Verify that no other application is using the printer

## Testing Different Printer Models

### Epson TM-T20/TM-T88 Series

```python
self.printers = {
    "main_kitchen": {
        "type": "printer", 
        "location": "Main Kitchen", 
        "enabled": True, 
        "connection": "USB",
        "vendor_id": 0x04b8,      # Epson vendor ID
        "product_id": 0x0e15,     # TM-T20/TM-T88 product ID
        "timeout": 0
    }
}
```

### Star Micronics TSP Series

```python
self.printers = {
    "main_kitchen": {
        "type": "printer", 
        "location": "Main Kitchen", 
        "enabled": True, 
        "connection": "USB",
        "vendor_id": 0x0519,      # Star Micronics vendor ID
        "product_id": 0x0002,     # TSP100 series product ID
        "timeout": 0
    }
}
```

## Performance Testing

To test printing performance:

```python
import time
from escpos.printer import Usb

def performance_test():
    start_time = time.time()
    
    try:
        printer = Usb(0x04b8, 0x0202, 0, 0x81, 0x03)
        
        # Print multiple KOTs
        for i in range(10):
            printer.text(f"Performance Test KOT #{i+1}\n")
            printer.text("=" * 40 + "\n")
            printer.text("Item 1 - Burger - $8.99\n")
            printer.text("Item 2 - Fries - $3.99\n")
            printer.text("-" * 40 + "\n")
            printer.text("Total: $12.98\n")
            printer.cut()
        
        printer.close()
        
        end_time = time.time()
        print(f"Printed 10 KOTs in {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        print(f"Performance test failed: {e}")

performance_test()
```

## Conclusion

This guide provides comprehensive instructions for testing the KOT system with physical printers. The system is designed to be flexible and work with various printer models and connection types. Always ensure you have the proper drivers and permissions before testing with physical hardware.