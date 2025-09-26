# Analytics API Documentation

This document describes the analytics endpoints available in the restaurant management system for tracking employee performance including sales, tips, and upselling metrics.

## Overview

The analytics API provides managers and administrators with insights into employee performance. All endpoints require authentication and are only accessible to users with MANAGER or ADMIN roles.

## Authentication

All analytics endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### 1. Get Sales by Employee

Retrieve sales data grouped by employee.

**Endpoint:** `GET /api/analytics/sales-by-employee`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
[
  {
    "employee_id": 1,
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "waiter",
    "order_count": 25,
    "total_sales": 1250.75,
    "average_order_value": 50.03
  }
]
```

### 2. Get Tips by Employee

Retrieve tip data grouped by employee.

**Endpoint:** `GET /api/analytics/tips-by-employee`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
[
  {
    "employee_id": 1,
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "waiter",
    "total_tips": 125.50,
    "tip_count": 20
  }
]
```

### 3. Get Upselling Performance

Retrieve upselling performance metrics by employee.

**Endpoint:** `GET /api/analytics/upselling-performance`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
[
  {
    "employee_id": 1,
    "username": "johndoe",
    "full_name": "John Doe",
    "role": "waiter",
    "upsell_count": 15,
    "upsell_revenue": 225.75
  }
]
```

### 4. Get Employee Performance Summary

Retrieve comprehensive performance summary for a specific employee.

**Endpoint:** `GET /api/analytics/employee/{employee_id}/performance`

**Parameters:**
- `employee_id` (path): The ID of the employee
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
{
  "employee_id": 1,
  "username": "johndoe",
  "full_name": "John Doe",
  "role": "waiter",
  "order_count": 25,
  "total_sales": 1250.75,
  "average_order_value": 50.03,
  "total_tips": 125.50,
  "upsell_count": 15
}
```

### 5. Get Daily Sales Report

Retrieve daily sales report with sales data grouped by day.

**Endpoint:** `GET /api/analytics/reports/daily`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
{
  "period": "daily",
  "start_date": "2023-01-01T00:00:00",
  "end_date": "2023-01-31T00:00:00",
  "total_sales": 25000.00,
  "total_orders": 500,
  "average_daily_sales": 806.45,
  "sales_data": [
    {
      "date": "2023-01-01T00:00:00",
      "total_sales": 1200.50,
      "order_count": 25,
      "average_order_value": 48.02
    }
  ]
}
```

### 6. Get Weekly Sales Report

Retrieve weekly sales report with sales data grouped by week.

**Endpoint:** `GET /api/analytics/reports/weekly`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
{
  "period": "weekly",
  "start_date": "2023-01-01T00:00:00",
  "end_date": "2023-03-31T00:00:00",
  "total_sales": 125000.00,
  "total_orders": 2500,
  "average_weekly_sales": 10000.00,
  "sales_data": [
    {
      "date": "2023-01-01T00:00:00",
      "total_sales": 12000.50,
      "order_count": 250,
      "average_order_value": 48.00
    }
  ]
}
```

### 7. Get Monthly Sales Report

Retrieve monthly sales report with sales data grouped by month.

**Endpoint:** `GET /api/analytics/reports/monthly`

**Parameters:**
- `start_date` (optional): Filter results from this date (ISO 8601 format)
- `end_date` (optional): Filter results until this date (ISO 8601 format)

**Response:**
```json
{
  "period": "monthly",
  "start_date": "2023-01-01T00:00:00",
  "end_date": "2023-12-31T00:00:00",
  "total_sales": 500000.00,
  "total_orders": 10000,
  "average_monthly_sales": 41666.67,
  "sales_data": [
    {
      "date": "2023-01-01T00:00:00",
      "total_sales": 50000.00,
      "order_count": 1000,
      "average_order_value": 50.00
    }
  ]
}
```

## Error Responses

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

Error responses follow the format:
```json
{
  "detail": "Error message"
}
```

## Implementation Notes

1. **Permissions**: Only users with MANAGER or ADMIN roles can access analytics endpoints.

2. **Date Filtering**: When using date filters, the system will include orders created between the specified dates (inclusive).

3. **Data Aggregation**: Sales data is aggregated from the orders table, grouping by the user who created each order.

4. **Placeholder Data**: Some endpoints currently return placeholder data as the full implementation requires additional database schema changes for tracking tips and upselling metrics.

5. **Role Filtering**: Analytics only include employees with roles that typically generate sales (WAITER, CASHIER, BAR).

## Future Enhancements

Planned improvements to the analytics system:

1. **Real Tip Tracking**: Implementation of a tips table or tip field in the orders table to track actual tip data.

2. **Upselling Metrics**: Addition of fields to track upsold items and their contribution to revenue.

3. **Advanced Filtering**: Additional filter options such as by shift, day of week, or specific menu categories.

4. **Export Functionality**: Ability to export analytics data in CSV or Excel format.

5. **Real-time Analytics**: WebSocket-based real-time performance tracking.

6. **Performance Benchmarks**: Comparison of employee performance against historical averages and targets.