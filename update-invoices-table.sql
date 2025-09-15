-- SQL script to create or update the invoices table to match the Invoice model
-- This script will handle both creating the table if it doesn't exist and updating it if it does

-- Create the invoices table with all required columns
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE,
    order_id INTEGER,
    customer_name TEXT,
    customer_phone TEXT,
    customer_address TEXT,
    order_type TEXT,
    table_number TEXT,
    subtotal REAL,
    tax REAL DEFAULT 0.0,
    total REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invoice_data TEXT,
    -- Add foreign key constraint if the orders table exists
    FOREIGN KEY (order_id) REFERENCES orders (id)
);

-- If the table already exists, we need to add any missing columns
-- Add invoice_number column if it doesn't exist
ALTER TABLE invoices ADD COLUMN invoice_number TEXT UNIQUE;
-- Add order_id column if it doesn't exist
ALTER TABLE invoices ADD COLUMN order_id INTEGER;
-- Add customer_name column if it doesn't exist
ALTER TABLE invoices ADD COLUMN customer_name TEXT;
-- Add customer_phone column if it doesn't exist
ALTER TABLE invoices ADD COLUMN customer_phone TEXT;
-- Add customer_address column if it doesn't exist
ALTER TABLE invoices ADD COLUMN customer_address TEXT;
-- Add order_type column if it doesn't exist
ALTER TABLE invoices ADD COLUMN order_type TEXT;
-- Add table_number column if it doesn't exist
ALTER TABLE invoices ADD COLUMN table_number TEXT;
-- Add subtotal column if it doesn't exist
ALTER TABLE invoices ADD COLUMN subtotal REAL;
-- Add tax column if it doesn't exist
ALTER TABLE invoices ADD COLUMN tax REAL DEFAULT 0.0;
-- Add total column if it doesn't exist
ALTER TABLE invoices ADD COLUMN total REAL;
-- Add created_at column if it doesn't exist
ALTER TABLE invoices ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- Add updated_at column if it doesn't exist
ALTER TABLE invoices ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
-- Add invoice_data column if it doesn't exist
ALTER TABLE invoices ADD COLUMN invoice_data TEXT;

-- Create index on invoice_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_number ON invoices (invoice_number);

-- Create index on order_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_order_id ON invoices (order_id);

-- Create index on created_at for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON invoices (created_at);