"""
Kitchen Order Ticket (KOT) Service
Handles sending orders to kitchen printers or display systems
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from models.order import OrderResponse
from models.kitchen import KitchenOrderDetail
from data.shared_data import sample_orders, sample_kitchen_orders

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KOTService:
    """Service for handling Kitchen Order Tickets"""
    
    def __init__(self):
        # In a real implementation, this would connect to actual printers or KDS
        self.printers = {
            "main_kitchen": {"type": "printer", "location": "Main Kitchen", "enabled": True},
            "grill_station": {"type": "printer", "location": "Grill Station", "enabled": True},
            "beverage_station": {"type": "kds", "location": "Beverage Station", "enabled": True},
            "dessert_station": {"type": "printer", "location": "Dessert Station", "enabled": True}
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
            
            # Add modifiers if they exist
            if hasattr(kitchen_order, 'modifiers') and kitchen_order.modifiers:
                # Try to get modifiers for this specific item
                item_modifiers = kitchen_order.modifiers.get(str(item.name), [])
                if not item_modifiers:
                    # Try with index-based approach
                    item_modifiers = kitchen_order.modifiers.get(str(i-1), [])
                if item_modifiers:
                    kot_content += f"   Modifiers: {', '.join(item_modifiers)}\n"
        
        # Special requests
        if hasattr(kitchen_order, 'special_requests') and kitchen_order.special_requests:
            kot_content += "-" * 40 + "\n"
            kot_content += f"Special Requests: {kitchen_order.special_requests}\n"
        
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
            
            # In a real implementation, this would send to an actual printer or KDS
            # For now, we'll just log it
            printer_info = self.printers[printer_id]
            logger.info(f"[KOT SERVICE] Sending to {printer_id} ({printer_info['type']} at {printer_info['location']}):")
            logger.info(kot_content)
            
            # Simulate successful sending
            return {"success": True, "message": f"KOT sent to {printer_id}", "content": kot_content}
        except Exception as e:
            error_msg = f"[KOT SERVICE] Error sending to printer {printer_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "message": error_msg}
    
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
        # Find the order and corresponding kitchen order
        order = next((o for o in sample_orders if o.id == order_id), None)
        kitchen_order_record = next((ko for ko in sample_kitchen_orders if ko.order_id == order_id), None)
        
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if not kitchen_order_record:
            raise ValueError(f"Order {order_id} not in kitchen")
        
        # Create KitchenOrderDetail object
        kitchen_order = KitchenOrderDetail(
            id=kitchen_order_record.id,
            order_id=kitchen_order_record.order_id,
            status=kitchen_order_record.status,
            created_at=kitchen_order_record.created_at,
            updated_at=kitchen_order_record.updated_at,
            order_items=order.order,
            total=order.total,
            order_type=getattr(order, 'order_type', 'dine-in'),
            table_number=getattr(order, 'table_number', None),
            customer_name=getattr(order, 'customer_name', None)
        )
        
        # Add modifiers and special requests if they exist
        if hasattr(order, 'modifiers'):
            kitchen_order.modifiers = order.modifiers
        if hasattr(order, 'special_requests'):
            kitchen_order.special_requests = order.special_requests
        
        # Route to appropriate stations
        return self.route_order_to_stations(kitchen_order)


# Global instance of KOTService
kot_service = KOTService()