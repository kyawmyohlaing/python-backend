# API Documentation

This document provides comprehensive documentation for all API endpoints in the restaurant management system.

## Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### Login
**POST** `/api/auth/login`
- Form data: username, password
- Returns: access_token, token_type

### Register
**POST** `/api/auth/register`
- JSON body: username, email, password, full_name, role
- Returns: User object

### Get Current User
**GET** `/api/auth/me`
- Returns: Current user information

## User Management

### List Users
**GET** `/api/auth/users`
- Requires authentication
- Returns: List of all users

### Get User
**GET** `/api/auth/users/{user_id}`
- Requires authentication
- Returns: User object

### Update User
**PUT** `/api/auth/users/{user_id}`
- Requires authentication
- JSON body: User fields to update
- Returns: Updated user object

### Delete User
**DELETE** `/api/auth/users/{user_id}`
- Requires authentication
- Returns: 204 No Content

## Menu Management

### List Menu Items
**GET** `/api/menu`
- Requires authentication
- Returns: List of all menu items

### Create Menu Item
**POST** `/api/menu`
- Requires authentication
- JSON body: name, price, category
- Returns: Created menu item

## Order Management

### List Orders
**GET** `/api/orders`
- Requires authentication
- Returns: List of all orders

### Create Order
**POST** `/api/orders`
- Requires authentication
- JSON body: table_number, order_type, order_items, payment_type
- Returns: Created order

**Payment Types:**
- `cash` - Cash payment
- `card` - Credit/debit card payment
- `qr` - QR code payment
- `e_wallet` - Electronic wallet payment
- `gift_card` - Gift card payment

### Get Order
**GET** `/api/orders/{order_id}`
- Requires authentication
- Returns: Order object

### Update Order
**PUT** `/api/orders/{order_id}`
- Requires authentication
- JSON body: Order fields to update (including payment_type)
- Returns: Updated order object

### Delete Order
**DELETE** `/api/orders/{order_id}`
- Requires authentication
- Returns: 204 No Content

## Table Management

### List Tables
**GET** `/api/tables`
- Requires authentication
- Returns: List of all tables

### Create Table
**POST** `/api/tables`
- Requires authentication
- JSON body: table_number, capacity
- Returns: Created table

### Get Table
**GET** `/api/tables/{table_id}`
- Requires authentication
- Returns: Table object

### Update Table
**PUT** `/api/tables/{table_id}`
- Requires authentication
- JSON body: Table fields to update
- Returns: Updated table object

### Delete Table
**DELETE** `/api/tables/{table_id}`
- Requires authentication
- Returns: 204 No Content

## Invoice Management

### List Invoices
**GET** `/api/invoices`
- Requires authentication
- Returns: List of all invoices

### Create Invoice
**POST** `/api/invoices`
- Requires authentication
- JSON body: order_id, customer_name, order_type, subtotal, total, invoice_items, payment_type
- Returns: Created invoice

**Payment Types:**
- `cash` - Cash payment
- `card` - Credit/debit card payment
- `qr` - QR code payment
- `e_wallet` - Electronic wallet payment
- `gift_card` - Gift card payment

### Get Invoice
**GET** `/api/invoices/{invoice_id}`
- Requires authentication
- Returns: Invoice object

### Get Invoice by Order ID
**GET** `/api/invoices/order/{order_id}`
- Requires authentication
- Returns: Invoice object

### Update Invoice
**PUT** `/api/invoices/{invoice_id}`
- Requires authentication
- JSON body: Invoice fields to update (including payment_type)
- Returns: Updated invoice object

### Delete Invoice
**DELETE** `/api/invoices/{invoice_id}`
- Requires authentication
- Returns: Success message

## Payment Management

### Process Payment
**POST** `/api/payments/process`
- Requires authentication
- JSON body: order_id, payment_type, amount, payment_details
- Returns: Payment processing result

**Payment Types:**
- `cash` - Cash payment
- `card` - Credit/debit card payment
- `qr` - QR code payment
- `e_wallet` - Electronic wallet payment
- `gift_card` - Gift card payment

### Refund Payment
**POST** `/api/payments/refund`
- Requires authentication
- JSON body: order_id, reason, refund_details
- Returns: Refund processing result

### Get Payment Methods
**GET** `/api/payments/methods`
- Requires authentication
- Returns: Available payment methods

### Get Payment Summary
**POST** `/api/payments/summary`
- Requires authentication
- JSON body: start_date, end_date (optional)
- Returns: Payment summary statistics

### Get Order Payment Status
**GET** `/api/payments/order/{order_id}`
- Requires authentication
- Returns: Payment status for the specified order

## Analytics

### Sales by Employee
**GET** `/api/analytics/sales-by-employee`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: List of employee sales data

### Tips by Employee
**GET** `/api/analytics/tips-by-employee`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: List of employee tip data

### Upselling Performance
**GET** `/api/analytics/upselling-performance`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: List of employee upselling performance data

### Employee Performance Summary
**GET** `/api/analytics/employee/{employee_id}/performance`
- Requires authentication (MANAGER or ADMIN role)
- Path parameter: employee_id
- Query parameters: start_date, end_date (optional)
- Returns: Comprehensive performance summary for the specified employee

### Daily Sales Report
**GET** `/api/analytics/reports/daily`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: Daily sales report with sales data grouped by day

### Weekly Sales Report
**GET** `/api/analytics/reports/weekly`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: Weekly sales report with sales data grouped by week

### Monthly Sales Report
**GET** `/api/analytics/reports/monthly`
- Requires authentication (MANAGER or ADMIN role)
- Query parameters: start_date, end_date (optional)
- Returns: Monthly sales report with sales data grouped by month

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