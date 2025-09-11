# Order Entry API Documentation

This document describes the Order Entry API functionality for Dine-in, Takeaway, and Delivery orders with support for modifiers.

## Overview

The Order Entry API allows creating, retrieving, updating, and deleting orders with different types (dine-in, takeaway, delivery) and modifiers for special requests like "no onions" or "extra cheese".

## Order Types

1. **Dine-in**: Orders consumed at the restaurant, requires a table number
2. **Takeaway**: Orders picked up by the customer, requires customer name and phone
3. **Delivery**: Orders delivered to a customer address, requires customer name, phone, and delivery address

## Modifiers

Modifiers are special requests that can be added to menu items, such as:
- "no onions"
- "extra cheese"
- "well done"
- "extra spicy"

## API Endpoints

### Create Order

**POST** `/api/orders`

Create a new order with the specified type and modifiers.

#### Request Body

```json
{
  "order": [
    {
      "name": "string",
      "price": "number",
      "category": "string",
      "modifiers": ["string"]
    }
  ],
  "total": "number",
  "order_type": "string", // "dine-in", "takeaway", or "delivery"
  "table_number": "string", // Required for dine-in orders
  "customer_name": "string", // Required for takeaway and delivery orders
  "customer_phone": "string", // Required for takeaway and delivery orders
  "delivery_address": "string" // Required for delivery orders
}
```

#### Response

```json
{
  "id": "integer",
  "order": [
    {
      "name": "string",
      "price": "number",
      "category": "string",
      "modifiers": ["string"]
    }
  ],
  "total": "number",
  "order_type": "string",
  "table_number": "string",
  "customer_name": "string",
  "customer_phone": "string",
  "delivery_address": "string",
  "timestamp": "datetime"
}
```

### Get All Orders

**GET** `/api/orders`

Retrieve all orders.

#### Response

Array of order objects as described above.

### Get Order by ID

**GET** `/api/orders/{order_id}`

Retrieve a specific order by its ID.

#### Response

Order object as described above.

### Update Order

**PUT** `/api/orders/{order_id}`

Update an existing order.

#### Request Body

Same structure as creating an order, but all fields are optional.

#### Response

Updated order object.

### Delete Order

**DELETE** `/api/orders/{order_id}`

Delete an order by its ID.

#### Response

```json
{
  "message": "Order deleted successfully"
}
```

## Examples

### Dine-in Order with Modifiers

```json
{
  "order": [
    {
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food",
      "modifiers": ["no onions", "extra cheese"]
    }
  ],
  "total": 2.5,
  "order_type": "dine-in",
  "table_number": "5",
  "customer_name": "John Doe",
  "customer_phone": "123-456-7890"
}
```

### Takeaway Order with Modifiers

```json
{
  "order": [
    {
      "name": "Mohinga",
      "price": 2.0,
      "category": "Myanmar Food",
      "modifiers": ["extra spicy"]
    },
    {
      "name": "Tea Leaf Salad",
      "price": 3.0,
      "category": "Myanmar Food",
      "modifiers": ["no peanuts"]
    }
  ],
  "total": 5.0,
  "order_type": "takeaway",
  "customer_name": "Jane Smith",
  "customer_phone": "987-654-3210"
}
```

### Delivery Order with Modifiers

```json
{
  "order": [
    {
      "name": "Shan Noodles",
      "price": 2.5,
      "category": "Myanmar Food",
      "modifiers": ["no onions"]
    },
    {
      "name": "Chicken Curry",
      "price": 4.5,
      "category": "Myanmar Food",
      "modifiers": ["extra cheese", "well done"]
    }
  ],
  "total": 7.0,
  "order_type": "delivery",
  "customer_name": "Bob Johnson",
  "customer_phone": "555-123-4567",
  "delivery_address": "123 Main St, City, State 12345"
}
```

## Testing

Tests for the Order Entry functionality are located in `tests/test_order_entry.py` and cover:
- Creating orders of all types with modifiers
- Retrieving orders
- Updating orders
- Deleting orders

Run tests with:
```
python -m pytest tests/test_order_entry.py
```