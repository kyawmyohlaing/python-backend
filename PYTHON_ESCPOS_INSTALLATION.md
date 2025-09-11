# Python ESC/POS Installation and Testing Guide

## Overview

This guide explains how to install and test the python-escpos library for physical printer integration with the KOT system.

## Installation

### Basic Installation

To install the python-escpos library:

```bash
pip install python-escpos
```

### System Dependencies (Linux)

For Linux systems, you may need to install additional system dependencies:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libusb-1.0-0-dev libudev-dev

# CentOS/RHEL/Fedora
sudo yum install libusb1-devel libudev-devel
# or for newer versions:
sudo dnf install libusb1-devel libudev-devel
```

### System Dependencies (Windows)

For Windows systems, you may need to install libusb:

1. Download libusb from http://libusb.info/
2. Extract and install the appropriate version for your system
3. Make sure the libusb DLL is in your PATH

### System Dependencies (macOS)

For macOS systems:

```bash
# Install Homebrew if you haven't already
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install libusb
brew install libusb
```

## Testing the Installation

### 1. Verify Installation

Create a simple test script to verify the installation:

```python
# test_escpos.py
try:
    from escpos.printer import Usb
    print("✓ python-escpos installed successfully")
except ImportError as e:
    print(f"✗ Failed to import python-escpos: {e}")
```

Run the test:
```bash
python test_escpos.py
```

### 2. Find Your Printer

#### On Linux:
```bash
lsusb
```

Look for your printer in the output. You'll see something like:
```
Bus 001 Device 005: ID 04b8:0202 Seiko Epson Corp. Receipt Printer M129C/TM-T20
```

In this example:
- Vendor ID: 04b8 (0x04b8)
- Product ID: 0202 (0x0202)

#### On Windows:
1. Open Device Manager
2. Expand "Universal Serial Bus controllers"
3. Look for your printer
4. Right-click and select "Properties"
5. Go to the "Details" tab
6. Select "Hardware Ids" from the dropdown
7. You'll see something like: `USB\VID_04B8&PID_0202`

#### On macOS:
```bash
system_profiler SPUSBDataType
```

### 3. Test Printer Connection

Create a test script for your specific printer:

```python
# printer_test.py
from escpos.printer import Usb

# Replace with your actual vendor and product IDs
VENDOR_ID = 0x04b8  # Example: Epson
PRODUCT_ID = 0x0202  # Example: TM-T20

try:
    # Connect to the printer
    # Parameters: vendor, product, timeout, in_ep, out_ep
    printer = Usb(VENDOR_ID, PRODUCT_ID, 0, 0x81, 0x03)
    
    # Print a test message
    printer.text("Printer Test Successful!\n")
    printer.text("This is a test of the KOT system.\n")
    printer.text("================================\n")
    printer.cut()
    
    # Close the connection
    printer.close()
    
    print("✓ Printer test completed successfully!")
    
except Exception as e:
    print(f"✗ Printer test failed: {e}")
```

### 4. Test Network Printer

If you're using a network printer:

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
    printer.text("================================\n")
    printer.cut()
    
    # Close the connection
    printer.close()
    
    print("✓ Network printer test completed successfully!")
    
except Exception as e:
    print(f"✗ Network printer test failed: {e}")
```

## Common Issues and Solutions

### 1. Permission Errors (Linux)

If you get permission errors:

```bash
# Add your user to the dialout group
sudo usermod -a -G dialout $USER

# Or create a udev rule for the printer
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0666"' | sudo tee /etc/udev/rules.d/99-escpos.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

# Then log out and log back in
```

### 2. Import Errors

If you get import errors:

```bash
# Reinstall with force
pip uninstall python-escpos pyusb
pip install python-escpos pyusb --no-cache-dir
```

### 3. USB Backend Errors

If you get USB backend errors:

```bash
# Install pyusb explicitly
pip install pyusb

# On Linux, you might need to install libusb explicitly
pip install libusb1
```

### 4. Printer Not Found

If the printer isn't detected:
1. Verify the vendor and product IDs are correct
2. Check that the printer is properly connected
3. Ensure the printer is powered on
4. Verify that no other application is using the printer

## Testing with the KOT System

Once you've verified that python-escpos is working, the KOT system will automatically use it for physical printer communication.

### 1. Update Printer Configuration

In [app/services/kot_service.py](file:///c:/strategy_test/python_backend_structure/app/services/kot_service.py), update your printer configuration:

```python
self.printers = {
    "main_kitchen": {
        "type": "printer", 
        "location": "Main Kitchen", 
        "enabled": True, 
        "connection": "USB",
        "vendor_id": 0x04b8,      # Your printer's vendor ID
        "product_id": 0x0202,     # Your printer's product ID
        "timeout": 0,
        "in_ep": 0x81,
        "out_ep": 0x03
    }
}
```

### 2. Test the Full KOT Workflow

Run the KOT printer test:

```bash
python test_kot_printer.py
```

You should see actual printing instead of simulation messages.

## Supported Printer Models

### Epson Printers
- TM-T20, TM-T88, TM-U220, etc.
- Vendor ID: 0x04b8
- Common Product IDs: 0x0202, 0x0e15

### Star Micronics Printers
- TSP100, TSP650, etc.
- Vendor ID: 0x0519
- Common Product IDs: 0x0002, 0x0003

### Other Brands
Check your printer's documentation for the correct vendor and product IDs.

## Performance Considerations

### Connection Management

For better performance, consider reusing printer connections:

```python
# In a production environment, you might want to maintain
# persistent connections rather than opening/closing for each print
```

### Error Handling

Implement robust error handling for production use:

```python
import time
from escpos.exceptions import USBNotFoundError, DeviceNotFoundError

def robust_print(printer_func, max_retries=3):
    """Attempt to print with retries"""
    for attempt in range(max_retries):
        try:
            printer_func()
            return True
        except (USBNotFoundError, DeviceNotFoundError) as e:
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry
                continue
            else:
                raise e
    return False
```

## Conclusion

This guide provides comprehensive instructions for installing and testing python-escpos with the KOT system. Once properly configured, the system will automatically use physical printers for KOT output, providing a realistic simulation of a restaurant POS environment.