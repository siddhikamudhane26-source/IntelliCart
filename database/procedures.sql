-- SQLite has no stored procedures. These MySQL 8 examples are supplied for DBMS viva/demo.
DELIMITER $$
CREATE PROCEDURE GetCustomerOrders(IN p_user_id INT)
BEGIN SELECT o.id AS order_id,o.total,o.status,o.created_at FROM orders o WHERE o.user_id=p_user_id ORDER BY o.created_at DESC; END$$
CREATE PROCEDURE GetTopProducts(IN p_limit INT)
BEGIN SELECT p.id,p.name,SUM(oi.quantity) units_sold,SUM(oi.quantity*oi.price) revenue FROM products p JOIN order_items oi ON oi.product_id=p.id GROUP BY p.id,p.name ORDER BY units_sold DESC LIMIT p_limit; END$$
DELIMITER ;
