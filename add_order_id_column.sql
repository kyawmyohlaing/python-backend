ALTER TABLE kitchen_orders ADD COLUMN order_id INTEGER;
ALTER TABLE kitchen_orders ADD CONSTRAINT fk_kitchen_orders_order_id FOREIGN KEY (order_id) REFERENCES orders(id);