#!/bin/bash
# Kitchen Orders Migration Script for Docker

echo "=== Kitchen Orders Migration for Docker ==="

# Check if running inside Docker container
if [ -f /.dockerenv ]; then
    echo "Running inside Docker container"
    cd /app
else
    echo "Running on host system"
    cd c:/strategy_test/python_backend_structure
fi

# Test database connection
echo "Testing database connection..."
python test_db_connection.py

if [ $? -ne 0 ]; then
    echo "Database connection test failed. Please check your database configuration."
    exit 1
fi

# Run migration
echo "Running kitchen orders table migration..."
python migrations/create_kitchen_orders_table.py

if [ $? -eq 0 ]; then
    echo "✅ Migration completed successfully!"
    echo "You can now restart your application to use the database-backed kitchen orders system."
else
    echo "❌ Migration failed!"
    exit 1
fi