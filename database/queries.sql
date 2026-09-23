-- IntelliCart SQL Implementation
SELECT * FROM products;
SELECT * FROM products WHERE category='Electronics';
SELECT * FROM products WHERE price BETWEEN 500 AND 5000 ORDER BY price;
SELECT category, COUNT(*) AS product_count FROM products GROUP BY category ORDER BY product_count DESC;
SELECT category, ROUND(AVG(price),2) AS average_price FROM products GROUP BY category;
SELECT * FROM products ORDER BY rating DESC LIMIT 10;
SELECT u.name, o.id AS order_id, o.total, o.status FROM users u JOIN orders o ON u.id=o.user_id;
SELECT o.id, u.name, p.name AS product, oi.quantity, oi.price FROM orders o JOIN users u ON u.id=o.user_id JOIN order_items oi ON oi.order_id=o.id JOIN products p ON p.id=oi.product_id;
SELECT ROUND(COALESCE(SUM(total),0),2) AS total_revenue FROM orders;
SELECT u.name, COUNT(o.id) AS orders, COALESCE(SUM(o.total),0) AS spending FROM users u LEFT JOIN orders o ON o.user_id=u.id GROUP BY u.id ORDER BY spending DESC;
SELECT p.name, SUM(oi.quantity) AS units_sold FROM products p JOIN order_items oi ON oi.product_id=p.id GROUP BY p.id ORDER BY units_sold DESC LIMIT 10;
SELECT p.category, ROUND(SUM(oi.quantity*oi.price),2) AS revenue FROM products p JOIN order_items oi ON oi.product_id=p.id GROUP BY p.category ORDER BY revenue DESC;
SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products);
SELECT name,email FROM users WHERE id IN (SELECT DISTINCT user_id FROM orders);
SELECT segment, COUNT(*) AS customers FROM users GROUP BY segment;
SELECT date(created_at) AS day, COUNT(*) AS orders, SUM(total) AS revenue FROM orders GROUP BY date(created_at) ORDER BY day;
