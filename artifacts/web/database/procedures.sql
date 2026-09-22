-- IntelliCart analytics procedures
--
-- SQLite does not support CREATE PROCEDURE. These parameterized query blocks
-- are the portable SQL procedures used by the Flask analytics layer. They are
-- kept in one file so the same business queries can be moved to PostgreSQL
-- stored procedures later without changing the dashboard contract.

-- Procedure: customer order history
SELECT
    o.id AS order_id,
    o.created_at,
    o.status,
    o.total_amount,
    GROUP_CONCAT(p.name, ', ') AS products
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
WHERE o.customer_id = :customer_id
GROUP BY o.id
ORDER BY o.created_at DESC;

-- Procedure: sales by category for a date range
SELECT
    c.name AS category,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
    SUM(oi.quantity) AS units_sold
FROM categories c
JOIN products p ON p.category_id = c.id
JOIN order_items oi ON oi.product_id = p.id
JOIN orders o ON o.id = oi.order_id
WHERE o.created_at BETWEEN :start_date AND :end_date
  AND o.status != 'cancelled'
GROUP BY c.id
HAVING SUM(oi.quantity * oi.unit_price) > 0
ORDER BY revenue DESC;

-- Procedure: customer RFM inputs
SELECT
    c.id,
    c.name,
    CAST(julianday('now') - julianday(MAX(o.created_at)) AS INTEGER) AS recency,
    COUNT(o.id) AS frequency,
    ROUND(COALESCE(SUM(o.total_amount), 0), 2) AS monetary
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE c.role = 'customer'
GROUP BY c.id
ORDER BY monetary DESC;