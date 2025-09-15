-- SQL script to update the orders table schema
-- This script adds missing columns to match the Order model definition

-- Add modifiers column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS modifiers TEXT;

-- Add order_type column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_type VARCHAR;

-- Add table_number column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS table_number VARCHAR;

-- Add customer_name column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_name VARCHAR;

-- Add customer_phone column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_phone VARCHAR;

-- Add delivery_address column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_address VARCHAR;

-- Add table_id column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS table_id INTEGER REFERENCES tables(id);

-- Add customer_count column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_count INTEGER DEFAULT 1;

-- Add special_requests column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS special_requests VARCHAR;

-- Add assigned_seats column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS assigned_seats VARCHAR;

-- Add timestamp column if it doesn't exist
ALTER TABLE orders ADD COLUMN IF NOT EXISTS timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Update existing rows to have default values for new columns
UPDATE orders SET order_type = 'dine-in' WHERE order_type IS NULL;
UPDATE orders SET customer_count = 1 WHERE customer_count IS NULL;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_orders_table_id ON orders(table_id);
CREATE INDEX IF NOT EXISTS idx_orders_timestamp ON orders(timestamp);
CREATE INDEX IF NOT EXISTS idx_orders_order_type ON orders(order_type);

-- Verify the table structure
-- \d orders;