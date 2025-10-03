# Payment API Documentation

This document describes the Payment API endpoints available in the restaurant management system.

## Overview

The Payment API provides endpoints for processing payments, handling refunds, retrieving payment methods, and getting payment summaries.

## Base URL

All URLs referenced in the documentation have the following base:

```
http://localhost:8088/api/payments
```

## Authentication

All endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Payment Methods

The system supports the following payment methods:

| Method     | Value      | Requires Processing | Instant Confirmation |
|------------|------------|---------------------|----------------------|
| Cash       | `cash`     | No                  | Yes                  |
| Card       | `card`     | Yes                 | No                   |
| QR Code    | `qr`       | Yes                 | No                   |
| E-Wallet   | `e_wallet` | Yes                 | No                   |
| Gift Card  | `gift_card`| Yes                 | No                   |

## Endpoints

### Process Payment

Process a payment for an order.

```
POST /process
```

#### Request Body

```json
{
  "order_id": 123,
  "payment_type": "card",
  "amount": 25.99,
  "payment_details": {
    "card_number": "**** **** **** 1234",
    "expiry_date": "12/25",
    "cvv": "***"
  }
}
```

#### Response

```json
{
  "success": true,
  "order_id": 123,
  "payment_type": "card",
  "amount": 25.99,
  "timestamp": "2025-10-01T10:30:00Z",
  "invoice_id": 456
}
```

### Refund Payment

Process a refund for a paid order.

```
POST /refund
```

#### Request Body

```json
{
  "order_id": 123,
  "reason": "Customer request",
  "refund_details": {
    "notes": "Customer changed their mind"
  }
}
```

#### Response

```json
{
  "success": true,
  "order_id": 123,
  "payment_type": "card",
  "refunded_amount": 25.99,
  "timestamp": "2025-10-01T11:30:00Z",
  "reference": "refund_1234567890"
}
```

### Get Payment Methods

Retrieve available payment methods.

```
GET /methods
```

#### Response

```json
{
  "cash": {
    "name": "Cash",
    "requires_processing": false,
    "instant_confirmation": true
  },
  "card": {
    "name": "Credit/Debit Card",
    "requires_processing": true,
    "instant_confirmation": false
  },
  "qr": {
    "name": "QR Code Payment",
    "requires_processing": true,
    "instant_confirmation": false
  },
  "e_wallet": {
    "name": "Electronic Wallet",
    "requires_processing": true,
    "instant_confirmation": false
  },
  "gift_card": {
    "name": "Gift Card",
    "requires_processing": true,
    "instant_confirmation": false
  }
}
```

### Get Payment Summary

Get payment summary statistics for a period.

```
POST /summary
```

#### Request Body

```json
{
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z"
}
```

#### Response

```json
{
  "success": true,
  "total_revenue": 5000.00,
  "total_transactions": 150,
  "payment_type_breakdown": {
    "cash": {
      "count": 50,
      "amount": 1250.00
    },
    "card": {
      "count": 60,
      "amount": 2500.00
    },
    "qr": {
      "count": 20,
      "amount": 750.00
    },
    "e_wallet": {
      "count": 15,
      "amount": 400.00
    },
    "gift_card": {
      "count": 5,
      "amount": 100.00
    }
  },
  "period": {
    "start_date": "2025-10-01T00:00:00Z",
    "end_date": "2025-10-31T23:59:59Z"
  }
}
```

### Get Order Payment Status

Get payment status for a specific order.

```
GET /order/{order_id}
```

#### Response

```json
{
  "order_id": 123,
  "payment_status": "completed",
  "payment_type": "card",
  "paid_at": "2025-10-01T10:30:00Z",
  "refund_status": null,
  "refunded_at": null
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Missing or invalid authentication
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses follow this format:

```json
{
  "detail": "Error message"
}
```

## Implementation Notes

1. **Payment Processing**: For payment methods that require processing (card, QR, e-wallet, gift card), the system simulates the processing. In a production environment, this would connect to actual payment processors.

2. **Validation**: All payment types are validated against the supported methods. Invalid payment types default to cash.

3. **Invoicing**: When a payment is processed, an invoice is automatically created if one doesn't already exist for the order.

4. **Refunds**: Refunds can only be processed for orders that have been successfully paid.

5. **Security**: All endpoints require authentication to prevent unauthorized access to payment functionality.