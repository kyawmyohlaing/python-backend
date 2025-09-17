"""
Kitchen Order Ticket (KOT) Service
Handles sending orders to kitchen printers or display systems
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from app.models.order import Order, OrderItem
from app.models.kitchen import KitchenOrder, KitchenOrderDetail

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import escpos for physical printer support
try:
    from escpos.printer import Usb, Network
    ESCPOS_AVAILABLE = True
except ImportError:
    ESCPOS_AVAILABLE = False
    logger.warning("python-escpos not installed. Physical printer support disabled.")

class KOTService:
    """Service for handling Kitchen Order Tickets"""
    
    def __init__(self):
        # In a real implementation, this would connect to actual printers or KDS
        self.printers = {
            "main_kitchen": {"type": "printer", "location": "Main Kitchen", "enabled": True, "connection": "USB", "vendor_id": 0x04b8, "product_id": 0x0202},
            "grill_station": {"type": "printer", "location": "Grill Station", "enabled": True, "connection": "USB", "vendor_id": 0x04b8, "product_id": 0x0202},
            "beverage_station": {"type": "kds", "location": "Beverage Station", "enabled": True, "connection": "network"},
            "dessert_station": {"type": "printer", "location": "Dessert Station", "enabled": True, "connection": "USB", "vendor_id": 0x04b8, "product_id": 0x0202}
        }
    
    def generate_kot_content(self, kitchen_order: KitchenOrderDetail) -> str:
        """
        Generate formatted KOT content for printing or display
        
        Args:
            kitchen_order: The kitchen order to generate KOT for
            
        Returns:
            Formatted KOT content as string
        """
        # Header
        kot_content = "=" * 40 + "\n"
        kot_content += "KITCHEN ORDER TICKET\n"
        kot_content += "=" * 40 + "\n"
        kot_content += f"Order ID: {kitchen_order.order_id}\n"
        kot_content += f"Time: {kitchen_order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        kot_content += f"Order Type: {kitchen_order.order_type or 'dine-in'}\n"
        
        if kitchen_order.table_number:
            kot_content += f"Table: {kitchen_order.table_number}\n"
        
        if kitchen_order.customer_name:
            kot_content += f"Customer: {kitchen_order.customer_name}\n"
        
        kot_content += "-" * 40 + "\n"
        
        # Order items
        kot_content += "ITEMS:\n"
        for i, item in enumerate(kitchen_order.order_items, 1):
            kot_content += f"{i}. {item.name} - ${item.price:.2f}\n"
            if hasattr(item, 'category') and item.category:
                kot_content += f"   Category: {item.category}\n"
            
            # Add modifiers if they exist (check multiple possible locations)
            modifiers = None
            if hasattr(kitchen_order, 'modifiers') and kitchen_order.modifiers:
                # Try to get modifiers for this specific item
                modifiers = kitchen_order.modifiers.get(item.name, [])
                if not modifiers:
                    # Try with index-based approach
                    modifiers = kitchen_order.modifiers.get(str(i-1), [])
            elif hasattr(item, 'modifiers') and item.modifiers:
                modifiers = item.modifiers
            
            if modifiers:
                kot_content += f"   Modifiers: {', '.join(modifiers)}\n"
        
        # Special requests
        special_requests = None
        if hasattr(kitchen_order, 'special_requests') and kitchen_order.special_requests:
            special_requests = kitchen_order.special_requests
        elif hasattr(kitchen_order, 'order') and hasattr(kitchen_order.order, 'special_requests'):
            special_requests = kitchen_order.order.special_requests
            
        if special_requests:
            kot_content += "-" * 40 + "\n"
            kot_content += f"Special Requests: {special_requests}\n"
        
        # Footer
        kot_content += "-" * 40 + "\n"
        kot_content += f"Status: {kitchen_order.status.upper()}\n"
        kot_content += f"Total: ${kitchen_order.total:.2f}\n"
        kot_content += "=" * 40 + "\n"
        
        return kot_content
    
    def send_to_printer(self, kitchen_order: KitchenOrderDetail, printer_id: str = "main_kitchen") -> Dict[str, any]:
        """
        Send KOT to a specific printer or KDS
        
        Args:
            kitchen_order: The kitchen order to send
            printer_id: ID of the printer/KDS to send to
            
        Returns:
            Dictionary with success status and message
        """
        try:
            # Check if printer exists and is enabled
            if printer_id not in self.printers:
                return {"success": False, "message": f"Printer {printer_id} not found"}
            
            if not self.printers[printer_id]["enabled"]:
                return {"success": False, "message": f"Printer {printer_id} is disabled"}
            
            # Generate KOT content
            kot_content = self.generate_kot_content(kitchen_order)
            
            # Get printer info
            printer_info = self.printers[printer_id]
            
            # Handle different types of output devices
            if printer_info["type"] == "kds":
                # For KDS, we might want to send structured data instead of plain text
                result = self._send_to_kds(kitchen_order, printer_id, kot_content)
            else:
                # For physical printers, send plain text
                result = self._send_to_physical_printer(kitchen_order, printer_id, kot_content)
            
            return result
        except Exception as e:
            error_msg = f"[KOT SERVICE] Error sending to {printer_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    def _send_to_physical_printer(self, kitchen_order: KitchenOrderDetail, printer_id: str, kot_content: str) -> Dict[str, any]:
        """
        Send KOT to a physical printer
        
        Args:
            kitchen_order: The kitchen order to send
            printer_id: ID of the printer to send to
            kot_content: Formatted KOT content
            
        Returns:
            Dictionary with success status and message
        """
        try:
            printer_info = self.printers[printer_id]
            
            # Check if escpos is available
            if not ESCPOS_AVAILABLE:
                logger.info(f"[KOT SERVICE] Escpos not available, simulating print to {printer_id} ({printer_info['location']})")
                logger.info(kot_content)
                return {"success": True, "message": f"Simulated print to {printer_id}", "content": kot_content}
            
            # Handle USB printer
            if printer_info.get("connection") == "USB":
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
                logger.info(f"[KOT SERVICE] Unknown connection type, simulating print to {printer_id} ({printer_info['location']})")
                logger.info(kot_content)
                return {"success": True, "message": f"Simulated print to {printer_id}", "content": kot_content}
                
        except Exception as e:
            error_msg = f"[KOT SERVICE] Error sending to physical printer {printer_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
    def _send_to_kds(self, kitchen_order: KitchenOrderDetail, kds_id: str, kot_content: str) -> Dict[str, any]:
        """
        Send KOT to a Kitchen Display System
        
        Args:
            kitchen_order: The kitchen order to send
            kds_id: ID of the KDS to send to
            kot_content: Formatted KOT content
            
        Returns:
            Dictionary with success status and message
        """
        try:
            kds_info = self.printers[kds_id]
            logger.info(f"[KOT SERVICE] Sending to KDS {kds_id} ({kds_info['location']}):")
            logger.info(kot_content)
            
            # For KDS, we might want to send structured data
            # In a real implementation, this could be:
            # 1. A direct API call to the KDS
            # 2. A message queue (like RabbitMQ or Kafka)
            # 3. A WebSocket connection
            # 4. A database update that the KDS monitors
            
            # Example structured data for KDS:
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
            
            # In a real implementation, you might do something like:
            # requests.post(f"http://{kds_info['ip_address']}/api/orders", json=kds_data)
            # or
            # websocket.send(json.dumps(kds_data))
            
            logger.info(f"[KOT SERVICE] KDS data: {json.dumps(kds_data, indent=2)}")
            
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
    
    def _get_item_modifiers(self, kitchen_order: KitchenOrderDetail, item) -> List[str]:
        """
        Extract modifiers for a specific item
        
        Args:
            kitchen_order: The kitchen order
            item: The menu item
            
        Returns:
            List of modifiers for the item
        """
        if hasattr(kitchen_order, 'modifiers') and kitchen_order.modifiers:
            # Try to get modifiers for this specific item
            modifiers = kitchen_order.modifiers.get(item.name, [])
            if not modifiers:
                # Try with index-based approach
                try:
                    item_index = kitchen_order.order_items.index(item)
                    modifiers = kitchen_order.modifiers.get(str(item_index), [])
                except ValueError:
                    pass
            return modifiers
        return []
    
    def route_order_to_stations(self, kitchen_order: KitchenOrderDetail) -> Dict[str, Dict[str, any]]:
        """
        Route order items to appropriate kitchen stations based on categories
        
        Args:
            kitchen_order: The kitchen order to route
            
        Returns:
            Dictionary mapping station IDs to result dictionaries
        """
        results = {}
        
        # Group items by category for routing to different stations
        station_items = {
            "main_kitchen": [],
            "grill_station": [],
            "beverage_station": [],
            "dessert_station": []
        }
        
        # Categorize items
        for item in kitchen_order.order_items:
            category = getattr(item, 'category', '').lower()
            if 'beverage' in category or 'drink' in category:
                station_items["beverage_station"].append(item)
            elif 'grill' in category or 'steak' in category or 'burger' in category:
                station_items["grill_station"].append(item)
            elif 'dessert' in category or 'sweet' in category:
                station_items["dessert_station"].append(item)
            else:
                station_items["main_kitchen"].append(item)
        
        # Send to appropriate stations
        for station_id, items in station_items.items():
            if items:  # Only send if there are items for this station
                # Create a copy of the kitchen order with only items for this station
                # We need to create a new object without the modifiers field that causes issues
                station_order = KitchenOrderDetail(
                    id=kitchen_order.id,
                    order_id=kitchen_order.order_id,
                    status=kitchen_order.status,
                    created_at=kitchen_order.created_at,
                    updated_at=kitchen_order.updated_at,
                    order_items=items,
                    total=sum(item.price for item in items),  # Recalculate total for this station
                    order_type=kitchen_order.order_type,
                    table_number=kitchen_order.table_number,
                    customer_name=kitchen_order.customer_name
                )
                results[station_id] = self.send_to_printer(station_order, station_id)
            else:
                results[station_id] = {"success": True, "message": f"No items for {station_id}"}
        
        return results
    
    def print_kot_for_order(self, order_id: int) -> Dict[str, Dict[str, any]]:
        """
        Generate and print KOT for a specific order
        
        Args:
            order_id: ID of the order to print KOT for
            
        Returns:
            Dictionary mapping station IDs to result dictionaries
        """
        # Get database session
        from app.database import SessionLocal
        db = SessionLocal()
        
        try:
            # Find the order and corresponding kitchen order from database
            order = db.query(Order).filter(Order.id == order_id).first()
            kitchen_order_record = db.query(KitchenOrder).filter(KitchenOrder.order_id == order_id).first()
            
            if not order:
                raise ValueError(f"Order {order_id} not found")
            
            if not kitchen_order_record:
                raise ValueError(f"Order {order_id} not in kitchen")
            
            # Convert order data from JSON
            order_items_dict = json.loads(order.order_data) if order.order_data else []
            
            # Convert to OrderItem objects
            order_items = [
                OrderItem(
                    name=item.get("name", ""),
                    price=item.get("price", 0.0),
                    category=item.get("category", ""),
                    modifiers=item.get("modifiers", [])
                ) for item in order_items_dict
            ]
            
            # Create KitchenOrderDetail object
            kitchen_order = KitchenOrderDetail(
                id=kitchen_order_record.id,
                order_id=kitchen_order_record.order_id,
                status=kitchen_order_record.status,
                created_at=kitchen_order_record.created_at,
                updated_at=kitchen_order_record.updated_at,
                order_items=order_items,
                total=order.total,
                order_type=getattr(order, 'order_type', 'dine-in'),
                table_number=getattr(order, 'table_number', None),
                customer_name=getattr(order, 'customer_name', None)
            )
            
            # Route to appropriate stations
            return self.route_order_to_stations(kitchen_order)
        finally:
            db.close()

    def get_printer_status(self, printer_id: str) -> Dict[str, any]:
        """
        Get the status of a specific printer or KDS
        
        Args:
            printer_id: ID of the printer/KDS to check
            
        Returns:
            Dictionary with status information
        """
        if printer_id not in self.printers:
            return {"success": False, "message": f"Printer {printer_id} not found"}
        
        printer_info = self.printers[printer_id]
        # In a real implementation, you would check actual printer status
        # For now, we'll just return the configured status
        return {
            "success": True,
            "printer_id": printer_id,
            "type": printer_info["type"],
            "location": printer_info["location"],
            "enabled": printer_info["enabled"],
            "connection": printer_info["connection"],
            "status": "online" if printer_info["enabled"] else "offline"
        }


# Global instance of KOTService
kot_service = KOTService()