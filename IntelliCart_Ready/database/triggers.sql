PRAGMA foreign_keys=ON;
CREATE TRIGGER IF NOT EXISTS trg_reduce_stock AFTER INSERT ON order_items BEGIN UPDATE products SET stock=stock-NEW.quantity WHERE id=NEW.product_id; END;
CREATE TRIGGER IF NOT EXISTS trg_update_customer_segment AFTER INSERT ON orders BEGIN UPDATE users SET segment=CASE WHEN (SELECT COALESCE(SUM(total),0) FROM orders WHERE user_id=NEW.user_id)>=10000 THEN 'VIP' WHEN (SELECT COUNT(*) FROM orders WHERE user_id=NEW.user_id)>=3 THEN 'Loyal' WHEN (SELECT COUNT(*) FROM orders WHERE user_id=NEW.user_id)>=1 THEN 'Active' ELSE 'New Customer' END WHERE id=NEW.user_id; END;
