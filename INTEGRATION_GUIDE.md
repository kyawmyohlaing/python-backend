# React Frontend Integration Guide

This document explains how to integrate the React frontend with the Python FastAPI backend.

## API Endpoints

The backend now provides the following API endpoints that match the frontend expectations:

### Menu Endpoints

1. **Get Menu Items**
   - URL: `/api/menu`
   - Method: `GET`
   - Description: Retrieve all available menu items
   - Response: Array of menu items

2. **Create Menu Item**
   - URL: `/api/menu`
   - Method: `POST`
   - Description: Create a new menu item
   - Request Body: Menu item data
   - Response: Created menu item with ID

### Order Endpoints

1. **Submit Order**
   - URL: `/api/orders`
   - Method: `POST`
   - Description: Submit a new order
   - Request Body: Order data
   - Response: Created order with ID and timestamp

2. **Get Orders**
   - URL: `/api/orders`
   - Method: `GET`
   - Description: Retrieve all submitted orders
   - Response: Array of all orders

3. **Get Specific Order**
   - URL: `/api/orders/{order_id}`
   - Method: `GET`
   - Description: Retrieve a specific order by ID
   - Response: Order details

4. **Update Order**
   - URL: `/api/orders/{order_id}`
   - Method: `PUT`
   - Description: Update an existing order
   - Request Body: Order update data
   - Response: Updated order

5. **Delete Order**
   - URL: `/api/orders/{order_id}`
   - Method: `DELETE`
   - Description: Delete an order
   - Response: Success message

### Kitchen Endpoints

1. **Get Kitchen Orders**
   - URL: `/api/kitchen/orders`
   - Method: `GET`
   - Description: Retrieve all orders for kitchen preparation
   - Response: Array of kitchen orders with details

2. **Update Order Status**
   - URL: `/api/kitchen/orders/{order_id}`
   - Method: `PUT`
   - Description: Update the status of a kitchen order
   - Request Body: Status update
   - Response: Updated kitchen order

3. **Remove Kitchen Order**
   - URL: `/api/kitchen/orders/{order_id}`
   - Method: `DELETE`
   - Description: Remove a completed order from the kitchen display
   - Response: Success message

### Table Management Endpoints

1. **Get All Tables**
   - URL: `/api/tables`
   - Method: `GET`
   - Description: Retrieve all tables in the restaurant
   - Response: Array of tables

2. **Get Specific Table**
   - URL: `/api/tables/{table_id}`
   - Method: `GET`
   - Description: Retrieve a specific table by ID
   - Response: Table details

3. **Create New Table**
   - URL: `/api/tables`
   - Method: `POST`
   - Description: Create a new table
   - Request Body: Table data
   - Response: Created table

4. **Update Table**
   - URL: `/api/tables/{table_id}`
   - Method: `PUT`
   - Description: Update a table's information
   - Request Body: Table update data
   - Response: Updated table

5. **Delete Table**
   - URL: `/api/tables/{table_id}`
   - Method: `DELETE`
   - Description: Delete a table (only if not occupied)
   - Response: Success message

6. **Assign Table to Order**
   - URL: `/api/tables/{table_id}/assign/{order_id}`
   - Method: `POST`
   - Description: Assign a table to an order
   - Response: Updated table

7. **Release Table**
   - URL: `/api/tables/{table_id}/release`
   - Method: `POST`
   - Description: Release a table (mark as available)
   - Response: Updated table

8. **Get Occupied Tables**
   - URL: `/api/tables/occupied`
   - Method: `GET`
   - Description: Retrieve all occupied tables
   - Response: Array of occupied tables

9. **Get Available Tables**
   - URL: `/api/tables/available`
   - Method: `GET`
   - Description: Retrieve all available tables
   - Response: Array of available tables

## Data Models

### Menu Item
```json
{
  "id": 1,
  "name": "Shan Noodles",
  "price": 2.5,
  "category": "Myanmar Food"
}
```

### Order
```json
{
  "id": 1,
  "order": [
    {
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food"
    }
  ],
  "total": 2.5,
  "table_id": 1,
  "customer_count": 2,
  "special_requests": "Extra spicy",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### Kitchen Order
```json
{
  "id": 1,
  "order_id": 1,
  "status": "pending",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "order_items": [
    {
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food"
    }
  ],
  "total": 2.5
}
```

### Table
```json
{
  "id": 1,
  "table_number": 1,
  "capacity": 4,
  "is_occupied": false,
  "current_order_id": null,
  "status": "available"
}
```

## Integration with Frontend

The frontend makes API calls to the `/api` endpoints, which are handled by the backend:

1. **Menu Page**: Fetches menu items from `/api/menu`
2. **Order Submission**: Sends order data to `/api/orders` (POST)
3. **Order History**: Fetches orders from `/api/orders` (GET)
4. **Kitchen Display**: Fetches and manages kitchen orders from `/api/kitchen/orders`
5. **Table Management**: Manages restaurant tables through `/api/tables` endpoints

## Running the Application

1. Start the backend server:
   ```bash
   # If using Docker
   docker-compose up
   
   # Or run directly
   python -m app.main
   ```

2. Start the frontend development server:
   ```bash
   cd ../react_frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

## Troubleshooting

### Pydantic Import Error

If you encounter the error:
```
Import "pydantic" could not be resolved basedpyright(reportMissingImports)
```

This means the pydantic library is not installed. To fix this:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Or install pydantic directly:
   ```bash
   pip install pydantic
   ```

### CORS Issues

If the frontend cannot communicate with the backend, ensure that CORS is properly configured in the backend and that the frontend is making requests to the correct URL.

### Port Conflicts

Ensure that the backend is running on the expected port (typically 8000 or 8088) and that this matches the proxy configuration in the frontend.