# Invoice API Documentation

## Overview

The Invoice API provides functionality for generating and managing invoices for completed orders in the restaurant POS system. This API allows you to create, retrieve, update, and delete invoices, as well as generate professional invoices from existing orders.

## API Endpoints

### Get All Invoices

**Endpoint:** `GET /api/invoices/`

**Description:** Retrieve all invoices in the system.

**Response:**
```json
[
  {
    "id": 1,
    "invoice_number": "INV-202305-0001",
    "order_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "123-456-7890",
    "customer_address": "123 Main St",
    "order_type": "dine-in",
    "table_number": "5",
    "subtotal": 20.50,
    "tax": 0.0,
    "total": 20.50,
    "created_at": "2023-05-01T10:30:00",
    "updated_at": "2023-05-01T10:30:00",
    "invoice_items": [
      {
        "name": "Burger",
        "category": "Main Course",
        "price": 12.00,
        "quantity": 1
      }
    ]
  }
]
```

### Get Invoice by ID

**Endpoint:** `GET /api/invoices/{invoice_id}`

**Description:** Retrieve a specific invoice by its ID.

**Parameters:**
- `invoice_id` (integer, required): The ID of the invoice to retrieve

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV-202305-0001",
  "order_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "123-456-7890",
  "customer_address": "123 Main St",
  "order_type": "dine-in",
  "table_number": "5",
  "subtotal": 20.50,
  "tax": 0.0,
  "total": 20.50,
  "created_at": "2023-05-01T10:30:00",
  "updated_at": "2023-05-01T10:30:00",
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    }
  ]
}
```

### Get Invoice by Order ID

**Endpoint:** `GET /api/invoices/order/{order_id}`

**Description:** Retrieve an invoice by its associated order ID.

**Parameters:**
- `order_id` (integer, required): The ID of the order associated with the invoice

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV-202305-0001",
  "order_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "123-456-7890",
  "customer_address": "123 Main St",
  "order_type": "dine-in",
  "table_number": "5",
  "subtotal": 20.50,
  "tax": 0.0,
  "total": 20.50,
  "created_at": "2023-05-01T10:30:00",
  "updated_at": "2023-05-01T10:30:00",
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    }
  ]
}
```

### Create Invoice

**Endpoint:** `POST /api/invoices/`

**Description:** Create a new invoice from an order.

**Request Body:**
```json
{
  "order_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "123-456-7890",
  "customer_address": "123 Main St",
  "order_type": "dine-in",
  "table_number": "5",
  "subtotal": 20.50,
  "tax": 0.0,
  "total": 20.50,
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV-202305-0001",
  "order_id": 1,
  "customer_name": "John Doe",
  "customer_phone": "123-456-7890",
  "customer_address": "123 Main St",
  "order_type": "dine-in",
  "table_number": "5",
  "subtotal": 20.50,
  "tax": 0.0,
  "total": 20.50,
  "created_at": "2023-05-01T10:30:00",
  "updated_at": "2023-05-01T10:30:00",
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    }
  ]
}
```

### Update Invoice

**Endpoint:** `PUT /api/invoices/{invoice_id}`

**Description:** Update an existing invoice.

**Parameters:**
- `invoice_id` (integer, required): The ID of the invoice to update

**Request Body:**
```json
{
  "customer_name": "Jane Smith",
  "customer_phone": "098-765-4321",
  "subtotal": 25.00,
  "total": 25.00,
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    },
    {
      "name": "Fries",
      "category": "Sides",
      "price": 5.00,
      "quantity": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "invoice_number": "INV-202305-0001",
  "order_id": 1,
  "customer_name": "Jane Smith",
  "customer_phone": "098-765-4321",
  "customer_address": "123 Main St",
  "order_type": "dine-in",
  "table_number": "5",
  "subtotal": 25.00,
  "tax": 0.0,
  "total": 25.00,
  "created_at": "2023-05-01T10:30:00",
  "updated_at": "2023-05-01T11:00:00",
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 12.00,
      "quantity": 1
    },
    {
      "name": "Fries",
      "category": "Sides",
      "price": 5.00,
      "quantity": 1
    }
  ]
}
```

### Delete Invoice

**Endpoint:** `DELETE /api/invoices/{invoice_id}`

**Description:** Delete an invoice.

**Parameters:**
- `invoice_id` (integer, required): The ID of the invoice to delete

**Response:**
```json
{
  "message": "Invoice deleted successfully"
}
```

## Data Models

### Invoice

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier for the invoice |
| invoice_number | string | Unique invoice number (e.g., INV-202305-0001) |
| order_id | integer | ID of the associated order |
| customer_name | string | Name of the customer |
| customer_phone | string (optional) | Customer's phone number |
| customer_address | string (optional) | Customer's address |
| order_type | string | Type of order (dine-in, takeaway, delivery) |
| table_number | string (optional) | Table number for dine-in orders |
| subtotal | float | Subtotal amount before tax |
| tax | float | Tax amount |
| total | float | Total amount including tax |
| created_at | datetime | Timestamp when invoice was created |
| updated_at | datetime | Timestamp when invoice was last updated |
| invoice_items | array | List of invoice items |

### InvoiceItem

| Field | Type | Description |
|-------|------|-------------|
| name | string | Name of the item |
| category | string | Category of the item |
| price | float | Price of the item |
| quantity | integer | Quantity of the item (default: 1) |

## Error Responses

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200`: Success
- `201`: Created
- `400`: Bad Request (e.g., invalid data, duplicate invoice)
- `404`: Not Found (e.g., invoice or order not found)
- `500`: Internal Server Error

Error responses follow this format:
```json
{
  "detail": "Error message"
}
```

## Implementation Details

### Invoice Number Generation

Invoice numbers are automatically generated in the format `INV-YYYYMM-XXXX` where:
- `YYYY` is the 4-digit year
- `MM` is the 2-digit month
- `XXXX` is a 4-digit sequential number starting from 0001

For example: `INV-202305-0001`

### Database Integration

The Invoice API integrates with the existing database schema and uses SQLAlchemy ORM for data persistence. The `Invoice` model is defined in `app/models/invoice.py` and includes all necessary fields for storing invoice information.

### Service Layer

The `InvoiceService` class in `app/services/invoice_service.py` provides business logic for invoice operations, including:
- Generating unique invoice numbers
- Creating invoices from existing orders
- Managing invoice items

## Usage Examples

### Creating an Invoice from an Order

```javascript
// JavaScript example using fetch API
const invoiceData = {
  order_id: 123,
  customer_name: "John Doe",
  customer_phone: "123-456-7890",
  order_type: "dine-in",
  table_number: "5",
  subtotal: 25.50,
  total: 25.50,
  invoice_items: [
    { name: "Burger", category: "Main Course", price: 12.00 },
    { name: "Fries", category: "Sides", price: 5.00 },
    { name: "Soda", category: "Drinks", price: 3.50 }
  ]
};

fetch('/api/invoices/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(invoiceData)
})
.then(response => response.json())
.then(data => console.log(data));
```

### Retrieving an Invoice

```javascript
// JavaScript example using fetch API
fetch('/api/invoices/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Updating an Invoice

```javascript
// JavaScript example using fetch API
const updateData = {
  customer_name: "Jane Smith",
  total: 30.00
};

fetch('/api/invoices/1', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(updateData)
})
.then(response => response.json())
.then(data => console.log(data));
```

## Testing

The Invoice API includes comprehensive tests in `tests/test_invoice_routes.py` that cover:
- Creating invoices from orders
- Retrieving invoices
- Updating invoices
- Deleting invoices
- Error handling for edge cases

To run the tests:
```bash
pytest tests/test_invoice_routes.py
```