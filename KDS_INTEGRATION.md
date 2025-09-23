# Kitchen Display System (KDS) and Printer Integration

This document describes the integration between the Kitchen Display System (KDS) and printer functionality in the FastAPI backend.

## 🖨️ Printer Management API

The system provides endpoints for managing and testing kitchen printers.

### Test Main Kitchen Printer

```bash
curl -X POST "http://localhost:8088/api/kitchen/printers/main_kitchen/test"
```

### Check Main Kitchen Printer Status

```bash
curl -X GET "http://localhost:8088/api/kitchen/printers/main_kitchen/status"
```

### Test Beverage Station Printer

```bash
curl -X POST "http://localhost:8088/api/kitchen/printers/beverage_station/test"
```

### Check Beverage Station Printer Status

```bash
curl -X GET "http://localhost:8088/api/kitchen/printers/beverage_station/status"
```

## 📋 Kitchen Order Management

### Mark Order as Served

```bash
curl -X POST "http://localhost:8088/api/kitchen/orders/1/mark-served"
```

## 🛠️ Implementation Details

### Printer Service

The printer service handles communication with physical printers and manages printer status.

### KDS Integration

The KDS integration provides real-time updates to kitchen displays when new orders are placed.

## 🧪 Testing

Use the provided cURL commands to test printer functionality and verify KDS integration.
