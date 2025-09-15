# API Documentation

This document provides a comprehensive overview of all available API endpoints in the FastAPI backend.

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## User Management

### Register a new user
**POST** `/api/users/register`
- Request body: `{ "username": "string", "email": "string", "password": "string" }`
- Response: User object with access token

### Login
**POST** `/api/users/login`
- Request body: `{ "username": "string", "password": "string" }`
- Response: Access token

### Get current user
**GET** `/api/users/me`
- Response: Current user object

## Menu Management

### Get all menu items
**GET** `/api/menu/`
- Response: Array of menu items

### Create a menu item
**POST** `/api/menu/`
- Request body: `{ "name": "string", "price": "number", "category": "string" }`
- Response: Created menu item

### Get menu item by ID
**GET** `/api/menu/{item_id}`
- Response: Menu item

### Update menu item
**PUT** `/api/menu/{item_id}`
- Request body: `{ "name": "string", "price": "number", "category": "string" }`
- Response: Updated menu item

### Delete menu item
**DELETE** `/api/menu/{item_id}`
- Response: Success message

### Get menu categories
**GET** `/api/menu/categories`
- Response: Array of category names

### Get menu items by category
**GET** `/api/menu/category/{category}`
- Response: Array of menu items in the specified category

### Create multiple menu items
**POST** `/api/menu/batch`
- Request body: Array of menu items
- Response: Array of created menu items

## Order Management

### Get all orders
**GET** `/api/orders/`
- Response: Array of orders

### Create an order
**POST** `/api/orders/`
- Request body: Order object
- Response: Created order

### Get order by ID
**GET** `/api/orders/{order_id}`
- Response: Order object

### Update order
**PUT** `/api/orders/{order_id}`
- Request body: Partial order object
- Response: Updated order

### Delete order
**DELETE** `/api/orders/{order_id}`
- Response: Success message

### Update order status
**PUT** `/api/orders/{order_id}/status`
- Request body: `{ "status": "string" }`
- Response: Updated order

### Mark order as served
**POST** `/api/orders/{order_id}/mark-served`
- Response: Success message

## Kitchen Display System (KDS)

### Get all kitchen orders
**GET** `/api/kitchen/orders`
- Response: Array of kitchen orders

### Get kitchen order by ID
**GET** `/api/kitchen/orders/{order_id}`
- Response: Kitchen order

### Update kitchen order status
**PUT** `/api/kitchen/orders/{order_id}`
- Request body: `{ "status": "string" }`
- Response: Updated kitchen order

### Remove kitchen order
**DELETE** `/api/kitchen/orders/{order_id}`
- Response: Success message

### Print Kitchen Order Ticket (KOT)
**POST** `/api/kitchen/orders/{order_id}/print-kot`
- Response: Success message

## Table Management

### Get all tables
**GET** `/api/tables/`
- Response: Array of tables

### Create a table
**POST** `/api/tables/`
- Request body: `{ "table_number": "integer", "capacity": "integer" }`
- Response: Created table

### Get table by ID
**GET** `/api/tables/{table_id}`
- Response: Table object

### Update table
**PUT** `/api/tables/{table_id}`
- Request body: Partial table object
- Response: Updated table

### Delete table
**DELETE** `/api/tables/{table_id}`
- Response: Success message

### Assign table to order
**POST** `/api/tables/{table_id}/assign/{order_id}`
- Response: Success message

### Release table
**POST** `/api/tables/{table_id}/release`
- Response: Success message

### Assign specific seat
**POST** `/api/tables/{table_id}/assign-seat/{seat_number}`
- Query parameter: `customer_name` (optional)
- Response: Success message

### Release specific seat
**POST** `/api/tables/{table_id}/release-seat/{seat_number}`
- Response: Success message

### Merge tables
**POST** `/api/tables/merge-tables/{table_id1}/{table_id2}`
- Response: Success message

### Split bill
**POST** `/api/tables/split-bill/{table_id}`
- Request body: Split details
- Response: Success message

### Get occupied tables
**GET** `/api/tables/occupied`
- Response: Array of occupied tables

### Get available tables
**GET** `/api/tables/available`
- Response: Array of available tables

## Invoice Management

### Get all invoices
**GET** `/api/invoices/`
- Response: Array of invoices

### Create an invoice
**POST** `/api/invoices/`
- Request body: Invoice object
- Response: Created invoice

### Get invoice by ID
**GET** `/api/invoices/{invoice_id}`
- Response: Invoice object

### Update invoice
**PUT** `/api/invoices/{invoice_id}`
- Request body: Partial invoice object
- Response: Updated invoice

### Delete invoice
**DELETE** `/api/invoices/{invoice_id}`
- Response: Success message

### Get invoice by order ID
**GET** `/api/invoices/order/{order_id}`
- Response: Invoice object

## Error Responses

All endpoints return appropriate HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

Error responses follow the format:
```json
{
  "detail": "Error message"
}
```