# Kitchen Display System (KDS) and Printer Integration

## Overview

This document provides detailed information on integrating Kitchen Display Systems (KDS) and physical printers with the existing Kitchen Order Tickets (KOT) system. The current implementation provides a flexible foundation that can be extended to work with various types of kitchen output devices.

## Current Implementation

The KOT system already distinguishes between different types of output devices:

```python
self.printers = {
    "main_kitchen": {"type": "printer", "location": "Main Kitchen", "enabled": True, "connection": "USB"},
    "grill_station": {"type": "printer", "location": "Grill Station", "enabled": True, "connection": "USB"},
    "beverage_station": {"type": "kds", "location": "Beverage Station", "enabled": True, "connection": "network"},
    "dessert_station": {"type": "printer", "location": "Dessert Station", "enabled": True, "connection": "USB"}
}
```

## Physical Printer Integration

### Supported Printer Types

The system can work with various types of physical printers commonly used in restaurant environments:

1. **Thermal Printers** - Most common in POS environments
2. **Dot Matrix Printers** - For multi-part order forms
3. **Label Printers** - For specific order items
4. **Network Printers** - For centralized printing solutions

### Implementation Example

To integrate with a physical thermal printer using the `python-escpos` library:

```python
# In app/services/kot_service.py, modify the _send_to_physical_printer method:

def _send_to_physical_printer(self, kitchen_order: KitchenOrderDetail, printer_id: str, kot_content: str) -> Dict[str, any]:
    """
    Send KOT to a physical printer
    """
    try:
        printer_info = self.printers[printer_id]
        
        # Example for USB thermal printer
        if printer_info.get("connection") == "USB":
            # Import the library (would need to be installed)
            # from escpos.printer import Usb
            
            # Connect to printer (example values)
            # p = Usb(0x04b8, 0x0202, 0, 0x81, 0x03)
            
            # Print content
            # p.text(kot_content)
            # p.cut()
            
            # Close connection
            # p.close()
            
            pass  # Placeholder for actual implementation
        
        # Example for network printer
        elif printer_info.get("connection") == "network":
            # Import the library
            # from escpos.printer import Network
            
            # Connect to network printer
            p = Network(printer_info.get("ip_address", "10.11.7.252"))
            
            # Print content
            # p.text(kot_content)
            # p.cut()
            
            # Close connection
            # p.close()
            
            pass  # Placeholder for actual implementation
        
        # Log the action
        logger.info(f"[KOT SERVICE] Sent to physical printer {printer_id} ({printer_info['location']})")
        
        # Simulate successful sending
        return {"success": True, "message": f"KOT sent to printer {printer_id}", "content": kot_content}
    except Exception as e:
        error_msg = f"[KOT SERVICE] Error sending to physical printer {printer_id}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "message": error_msg}
```

### Required Dependencies

To implement physical printer integration, you would need to add these dependencies to your `requirements.txt`:

```txt
python-escpos>=3.0
pyusb>=1.0  # For USB printers
```

## Kitchen Display System (KDS) Integration

### KDS Communication Methods

The system supports multiple methods for communicating with Kitchen Display Systems:

1. **REST API Calls** - Direct HTTP requests to KDS endpoints
2. **WebSocket Connections** - Real-time bidirectional communication
3. **Message Queues** - Using systems like RabbitMQ or Apache Kafka
4. **Database Polling** - KDS systems that monitor database changes

### Implementation Example

To integrate with a KDS using REST API calls:

```python
# In app/services/kot_service.py, modify the _send_to_kds method:

def _send_to_kds(self, kitchen_order: KitchenOrderDetail, kds_id: str, kot_content: str) -> Dict[str, any]:
    """
    Send KOT to a Kitchen Display System
    """
    try:
        kds_info = self.printers[kds_id]
        
        # Prepare structured data for KDS
        kds_data = {
            "order_id": kitchen_order.order_id,
            "kds_id": kds_id,
            "items": [
                {
                    "name": item.name,
                    "price": item.price,
                    "category": getattr(item, 'category', ''),
                    "modifiers": self._get_item_modifiers(kitchen_order, item)
                }
                for item in kitchen_order.order_items
            ],
            "table_number": kitchen_order.table_number,
            "customer_name": kitchen_order.customer_name,
            "order_type": kitchen_order.order_type,
            "timestamp": kitchen_order.created_at.isoformat(),
            "status": kitchen_order.status
        }
        
        # Example REST API integration
        if kds_info.get("connection") == "network":
            import requests
            
            # Get KDS endpoint
            kds_endpoint = kds_info.get("endpoint", f"http://kds-{kds_id}.local/api/orders")
            
            # Send data to KDS
            response = requests.post(kds_endpoint, json=kds_data, timeout=5)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"KOT sent to KDS {kds_id}",
                    "content": kot_content,
                    "kds_data": kds_data,
                    "kds_response": response.json()
                }
            else:
                return {
                    "success": False,
                    "message": f"KDS {kds_id} returned status {response.status_code}",
                    "content": kot_content,
                    "kds_data": kds_data
                }
        
        # Example WebSocket integration
        elif kds_info.get("connection") == "websocket":
            # This would require maintaining WebSocket connections
            # import websockets
            # async with websockets.connect(kds_info.get("websocket_url")) as websocket:
            #     await websocket.send(json.dumps(kds_data))
            
            pass  # Placeholder for actual implementation
        
        # Log the action
        logger.info(f"[KOT SERVICE] Sent to KDS {kds_id} ({kds_info['location']})")
        
        # Simulate successful sending
        return {
            "success": True,
            "message": f"KOT sent to KDS {kds_id}",
            "content": kot_content,
            "kds_data": kds_data
        }
    except Exception as e:
        error_msg = f"[KOT SERVICE] Error sending to KDS {kds_id}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "message": error_msg}
```

### KDS Configuration

To configure a KDS in the system, add it to the printers configuration:

```python
self.printers = {
    "beverage_station": {
        "type": "kds",
        "location": "Beverage Station",
        "enabled": True,
        "connection": "network",
        "endpoint": "http://beverage-kds.local/api/orders",
        "websocket_url": "ws://beverage-kds.local/ws"
    }
}
```

## Testing Integration

### Printer Testing

The system includes endpoints for testing printer connectivity:

```bash
# Test a specific printer
curl -X POST "http://localhost:8000/api/kitchen/printers/main_kitchen/test"

# Get printer status
curl -X GET "http://localhost:8000/api/kitchen/printers/main_kitchen/status"
```

### KDS Testing

Similar endpoints exist for testing KDS connectivity:

```bash
# Test a specific KDS
curl -X POST "http://localhost:8000/api/kitchen/printers/beverage_station/test"

# Get KDS status
curl -X GET "http://localhost:8000/api/kitchen/printers/beverage_station/status"
```

## Extending the System

### Adding New Printer Types

To add support for new types of printers or KDS systems:

1. Update the printer configuration in `kot_service.py`
2. Modify the `send_to_printer` method to handle the new type
3. Implement specific sending methods for the new type
4. Add appropriate error handling and logging

### Example: Adding Bluetooth Printer Support

```python
def _send_to_bluetooth_printer(self, kitchen_order: KitchenOrderDetail, printer_id: str, kot_content: str) -> Dict[str, any]:
    """
    Send KOT to a Bluetooth printer
    """
    try:
        printer_info = self.printers[printer_id]
        
        # Example using bluetooth library
        # import bluetooth
        
        # Connect to Bluetooth printer
        # sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        # sock.connect((printer_info.get("bluetooth_address"), printer_info.get("bluetooth_channel", 1)))
        
        # Send content
        # sock.send(kot_content.encode())
        
        # Close connection
        # sock.close()
        
        # Log the action
        logger.info(f"[KOT SERVICE] Sent to Bluetooth printer {printer_id}")
        
        # Simulate successful sending
        return {"success": True, "message": f"KOT sent to Bluetooth printer {printer_id}", "content": kot_content}
    except Exception as e:
        error_msg = f"[KOT SERVICE] Error sending to Bluetooth printer {printer_id}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "message": error_msg}
```

## Error Handling and Monitoring

The system includes comprehensive error handling and logging:

1. **Connection Errors** - Network issues, device offline
2. **Device Errors** - Printer out of paper, hardware malfunctions
3. **Data Errors** - Malformed KOT content, invalid order data
4. **Timeout Errors** - Slow responses from devices

### Monitoring Integration

The system logs all KOT activities, which can be integrated with monitoring systems:

```python
# Example integration with monitoring system
def _log_kot_activity(self, activity_type: str, details: dict):
    """
    Log KOT activity for monitoring
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "activity_type": activity_type,
        "details": details
    }
    
    # Send to monitoring system
    # monitoring_client.send(log_entry)
    
    # Or write to file
    # with open("kot_activity.log", "a") as f:
    #     f.write(json.dumps(log_entry) + "\n")
```

## Security Considerations

When integrating with external devices:

1. **Network Security** - Use HTTPS for API calls, secure WebSocket connections
2. **Authentication** - Implement API keys or tokens for device communication
3. **Data Validation** - Validate all data before sending to devices
4. **Access Control** - Restrict which systems can send KOTs

### Example: Adding Authentication

```python
def _send_to_kds(self, kitchen_order: KitchenOrderDetail, kds_id: str, kot_content: str) -> Dict[str, any]:
    """
    Send KOT to a Kitchen Display System with authentication
    """
    try:
        kds_info = self.printers[kds_id]
        
        # Prepare structured data for KDS
        kds_data = {
            # ... data preparation ...
        }
        
        # Add authentication headers
        headers = {
            "Authorization": f"Bearer {kds_info.get('api_key')}",
            "Content-Type": "application/json"
        }
        
        # Send data to KDS with authentication
        response = requests.post(
            kds_info.get("endpoint"),
            json=kds_data,
            headers=headers,
            timeout=5
        )
        
        # ... rest of implementation ...
```

## Performance Considerations

1. **Asynchronous Operations** - Use async/await for non-blocking device communication
2. **Connection Pooling** - Reuse connections to devices when possible
3. **Batch Processing** - Combine multiple KOTs when sending to the same device
4. **Caching** - Cache device status and capabilities

### Example: Asynchronous Implementation

```python
import asyncio
import aiohttp

async def _send_to_kds_async(self, kitchen_order: KitchenOrderDetail, kds_id: str, kot_content: str) -> Dict[str, any]:
    """
    Asynchronously send KOT to a Kitchen Display System
    """
    try:
        kds_info = self.printers[kds_id]
        
        # Prepare structured data for KDS
        kds_data = {
            # ... data preparation ...
        }
        
        # Send data asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.post(kds_info.get("endpoint"), json=kds_data) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "message": f"KOT sent to KDS {kds_id}",
                        "content": kot_content,
                        "kds_data": kds_data,
                        "kds_response": result
                    }
                else:
                    return {
                        "success": False,
                        "message": f"KDS {kds_id} returned status {response.status}",
                        "content": kot_content,
                        "kds_data": kds_data
                    }
    except Exception as e:
        error_msg = f"[KOT SERVICE] Error sending to KDS {kds_id}: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "message": error_msg}
```

## Conclusion

The KOT system provides a flexible foundation for integrating with various kitchen output devices. The modular design allows for easy extension to support new types of printers and KDS systems. The implementation includes comprehensive error handling, logging, and testing capabilities to ensure reliable operation in a restaurant environment.

To implement specific integrations, you would need to:

1. Choose the appropriate communication method for your devices
2. Install required libraries and dependencies
3. Configure device connection details
4. Implement device-specific sending methods
5. Test the integration thoroughly