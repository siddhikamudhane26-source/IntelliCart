-- Reduce stock automatically whenever a paid order item is inserted.
-- The checkout route validates stock before inserting, while this trigger keeps
-- direct SQL inserts safe for demos and future admin tooling.

CREATE TRIGGER IF NOT EXISTS reduce_product_stock
AFTER INSERT ON order_items
BEGIN
    UPDATE products
    SET stock = MAX(0, stock - NEW.quantity)
    WHERE id = NEW.product_id;

    INSERT INTO interactions (customer_id, product_id, interaction_type)
    SELECT o.customer_id, NEW.product_id, 'purchase'
    FROM orders o
    WHERE o.id = NEW.order_id;
END;

CREATE TRIGGER IF NOT EXISTS refresh_product_rating
AFTER INSERT ON reviews
BEGIN
    UPDATE products
    SET
        rating = (
            SELECT ROUND(AVG(rating), 2)
            FROM reviews
            WHERE product_id = NEW.product_id
        ),
        review_count = (
            SELECT COUNT(*)
            FROM reviews
            WHERE product_id = NEW.product_id
        )
    WHERE id = NEW.product_id;
END;