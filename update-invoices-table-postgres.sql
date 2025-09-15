-- SQL script to create or update the invoices table to match the Invoice model
-- This script is compatible with PostgreSQL

-- Create the invoices table with all required columns
CREATE TABLE IF NOT EXISTS invoices (
    id SERIAL PRIMARY KEY,
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

-- Create index on invoice_number for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_invoice_number ON invoices (invoice_number);

-- Create index on order_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_order_id ON invoices (order_id);

-- Create index on created_at for faster lookups
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON invoices (created_at);

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at when row is modified
DROP TRIGGER IF EXISTS update_invoices_updated_at ON invoices;
CREATE TRIGGER update_invoices_updated_at 
    BEFORE UPDATE ON invoices 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();