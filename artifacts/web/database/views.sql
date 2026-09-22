-- Read-only analytics views used by the admin dashboard.

DROP VIEW IF EXISTS dashboard_summary;
CREATE VIEW dashboard_summary AS
SELECT
    (SELECT COALESCE(SUM(total_amount), 0) FROM orders WHERE status != 'cancelled') AS revenue,
    (SELECT COUNT(*) FROM orders) AS orders,
    (SELECT COUNT(*) FROM customers WHERE role = 'customer') AS customers,
    (SELECT COUNT(*) FROM products) AS products,
    (SELECT COALESCE(AVG(total_amount), 0) FROM orders WHERE status != 'cancelled') AS average_order_value;

DROP VIEW IF EXISTS monthly_sales;
CREATE VIEW monthly_sales AS
SELECT
    strftime('%Y-%m', created_at) AS month,
    ROUND(SUM(total_amount), 2) AS revenue,
    COUNT(*) AS orders
FROM orders
WHERE status != 'cancelled'
GROUP BY strftime('%Y-%m', created_at);

DROP VIEW IF EXISTS category_sales;
CREATE VIEW category_sales AS
SELECT
    c.name AS category,
    ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS revenue,
    COALESCE(SUM(oi.quantity), 0) AS units
FROM categories c
LEFT JOIN products p ON p.category_id = c.id
LEFT JOIN order_items oi ON oi.product_id = p.id
GROUP BY c.id;

DROP VIEW IF EXISTS top_products;
CREATE VIEW top_products AS
SELECT
    p.name,
    c.name AS category,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    ROUND(COALESCE(SUM(oi.quantity * oi.unit_price), 0), 2) AS revenue
FROM products p
JOIN categories c ON c.id = p.category_id
LEFT JOIN order_items oi ON oi.product_id = p.id
GROUP BY p.id;