# Kitchen Order Tickets (KOT) System

## Overview

The Kitchen Order Tickets (KOT) system is a comprehensive solution for sending orders directly from the POS system to kitchen printers or display systems (KDS). This system automatically routes order items to appropriate kitchen stations based on item categories, ensuring efficient order processing in restaurant environments.

## System Architecture

The KOT system consists of several components working together:

1. **KOT Service** - Core logic for generating and routing KOTs
2. **Kitchen Routes** - API endpoints for KOT operations
3. **Frontend Integration** - UI components for manual KOT printing
4. **Automatic Integration** - Seamless KOT generation on order creation

## Key Features

### 1. Automatic Order Routing
Orders are automatically routed to appropriate kitchen stations based on item categories:
- **Main Kitchen**: General food items
- **Grill Station**: Grilled items (burgers, steaks, etc.)
- **Beverage Station**: Drinks (sent to KDS)
- **Dessert Station**: Desserts and sweets

### 2. Multi-Station Support
Different types of items are sent to specialized stations for efficient preparation.

### 3. Printer Management
Support for both physical printers and digital display systems (KDS).

### 4. Testing Capabilities
Ability to test printer connectivity to ensure system reliability.

### 5. Detailed Reporting
Comprehensive feedback on KOT printing status for each station.

## Implementation Details

### Backend Components

#### KOT Service (`app/services/kot_service.py`)
The core service responsible for:
- Generating formatted KOT content
- Routing orders to appropriate kitchen stations
- Managing printer connections
- Handling errors and logging

#### Kitchen Routes (`app/routes/kitchen_routes.py`)
API endpoints for KOT operations:
- `GET /api/kitchen/printers` - Get printer information
- `POST /api/kitchen/printers/{printer_id}/test` - Test printer connectivity
- `POST /api/kitchen/orders/{order_id}/print-kot` - Generate and print KOT

#### Order Integration (`app/routes/order_routes.py`)
Automatic KOT printing when orders are created.

### Frontend Components

#### Kitchen Page (`src/KitchenPage.jsx`)
UI for kitchen staff with:
- Order status management
- Manual KOT printing capabilities
- Real-time order updates

#### API Integration (`src/api.js`)
[printKOT](file:///c:/strategy_test/react_frontend/src/api.js#L201-L215) function for communicating with the backend KOT printing endpoint.

## API Endpoints

### Get Kitchen Printers
```
GET /api/kitchen/printers
```
Returns information about all configured kitchen printers and KDS systems.

### Test Printer Connectivity
```
POST /api/kitchen/printers/{printer_id}/test
```
Tests connectivity to a specific printer or KDS.

### Print Kitchen Order Ticket
```
POST /api/kitchen/orders/{order_id}/print-kot
```
Generates and prints a KOT for a specific order, routing items to appropriate stations.

## KOT Content Format

The generated KOTs follow this format:
```
========================================
KITCHEN ORDER TICKET
========================================
Order ID: 101
Time: 2025-09-11 15:40:40
Order Type: dine-in
Table: 5
Customer: John Doe
----------------------------------------
ITEMS:
1. Burger - $8.99
   Category: Main Course
   Modifiers: Extra Cheese, No Onion
2. Fries - $3.99
   Category: Sides
3. Soda - $2.99
   Category: Beverages
   Modifiers: Extra Ice
----------------------------------------
Special Requests: All food well done, please
----------------------------------------
Status: PENDING
Total: $15.97
========================================
```

## Testing

The system includes comprehensive testing capabilities:
1. Unit tests for KOT generation
2. Integration tests for printer routing
3. API endpoint tests
4. Manual testing through the frontend UI

## Future Enhancements

Potential improvements for the KOT system:
1. Integration with actual printer hardware
2. Support for more specialized kitchen stations
3. Enhanced KOT formatting options
4. Real-time KOT status updates
5. KOT reprinting capabilities
6. Integration with inventory management systems

## Troubleshooting

Common issues and solutions:
1. **Printer Not Found**: Verify printer configuration in KOT service
2. **Routing Issues**: Check category mappings in routing logic
3. **Formatting Problems**: Review KOT content generation function
4. **Connectivity Issues**: Use the printer test endpoint to diagnose problems

## Conclusion

The KOT system provides a robust foundation for restaurant kitchen order management, enabling efficient communication between front-of-house and back-of-house operations. Its modular design allows for easy extension and customization to meet specific restaurant requirements.