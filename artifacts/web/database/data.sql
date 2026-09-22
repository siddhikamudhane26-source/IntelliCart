-- IntelliCart starter data

INSERT INTO customers (name, email) VALUES
    ('Aarav Mehta', 'aarav@example.com'),
    ('Maya Shah', 'maya@example.com');

INSERT INTO products (name, category, price) VALUES
    ('Everyday Carry Backpack', 'Accessories', 79.00),
    ('Wireless Desk Lamp', 'Home Office', 54.50),
    ('Ceramic Pour-Over Set', 'Kitchen', 42.00);

INSERT INTO interactions (customer_id, product_id, interaction_type) VALUES
    (1, 1, 'view'),
    (1, 2, 'save'),
    (2, 3, 'view');