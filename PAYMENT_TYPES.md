# Payment Types Implementation

This document describes the implementation of multiple payment types support in the restaurant management system.

## Overview

The system now supports multiple payment types for orders and invoices:
- Cash
- Credit/Debit Card
- QR Code Payment
- Electronic Wallet (E-Wallet)
- Gift Card

## Implementation Details

### Database Changes

1. **Orders Table**: Added `payment_type` column with enum type
2. **Invoices Table**: Added `payment_type` column with string type

### Models

1. **Order Model**: Added `payment_type` field with enum values
2. **Invoice Model**: Added `payment_type` field with string type

### Schemas

1. **Order Schema**: Added `payment_type` field with default value "cash"
2. **Invoice Schema**: Added `payment_type` field with default value "cash"

### Services

1. **Invoice Service**: Updated to inherit payment type from the associated order when creating invoices

### Routes

1. **Order Routes**: Added validation for payment types
2. **Invoice Routes**: Added validation for payment types

## Supported Payment Types

| Payment Type | Value      | Description                  |
|--------------|------------|------------------------------|
| Cash         | `cash`     | Physical cash payment        |
| Card         | `card`     | Credit/debit card payment    |
| QR Code      | `qr`       | QR code payment              |
| E-Wallet     | `e_wallet` | Electronic wallet payment    |
| Gift Card    | `gift_card`| Gift card payment            |

## API Usage

### Creating Orders with Payment Types

When creating an order, you can specify the payment type:

```json
{
  "order": [
    {
      "name": "Burger",
      "price": 8.99,
      "category": "Main Course"
    }
  ],
  "total": 8.99,
  "payment_type": "card"
}
```

### Updating Order Payment Types

You can update an order's payment type:

```json
{
  "payment_type": "qr"
}
```

### Creating Invoices with Payment Types

When creating an invoice, the payment type will be inherited from the associated order, but can also be explicitly set:

```json
{
  "order_id": 123,
  "customer_name": "John Doe",
  "order_type": "dine_in",
  "subtotal": 8.99,
  "total": 8.99,
  "invoice_items": [
    {
      "name": "Burger",
      "category": "Main Course",
      "price": 8.99,
      "quantity": 1
    }
  ],
  "payment_type": "card"
}
```

## Validation

The system validates payment types and defaults to "cash" for invalid values.

## Migration

Database migrations have been created to add the payment_type column to both orders and invoices tables.

## Testing

Unit tests have been added to verify:
1. Creating orders with different payment types
2. Updating order payment types
3. Invalid payment types defaulting to cash
4. Invoices inheriting payment types from orders