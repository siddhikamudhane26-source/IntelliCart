-- IntelliCart realistic demo data.
-- The recursive inserts keep this file compact while generating:
-- 30 customers, 10 categories, 60 products, 120 orders, order items,
-- payments, reviews, and interaction events.

INSERT OR IGNORE INTO customers (name, email, password_hash, phone, city, role) VALUES
    ('Aarav Mehta', 'admin@intellicart.com', 'scrypt:32768:8:1$xDBnxBHd26d1gdTU$51314fa5779501e77bc0223f3f6ea764784720af5bf47857d65658a2676401ecb682b42816fcdd845370d567d72360bfbd7a67baea77a1bc60b3c12324bc326e', '+91 98765 00001', 'Mumbai', 'admin'),
    ('Maya Shah', 'maya.shah@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00002', 'Pune', 'customer'),
    ('Ishaan Kapoor', 'ishaan.kapoor@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42b10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00003', 'Delhi', 'customer'),
    ('Ananya Iyer', 'ananya.iyer@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00004', 'Bengaluru', 'customer'),
    ('Rohan Malhotra', 'rohan.malhotra@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00005', 'Chandigarh', 'customer'),
    ('Kavya Nair', 'kavya.nair@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00006', 'Kochi', 'customer'),
    ('Dev Patel', 'dev.patel@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00007', 'Ahmedabad', 'customer'),
    ('Diya Banerjee', 'diya.banerjee@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00008', 'Kolkata', 'customer'),
    ('Aditya Rao', 'aditya.rao@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00009', 'Hyderabad', 'customer'),
    ('Saanvi Joshi', 'saanvi.joshi@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00010', 'Jaipur', 'customer'),
    ('Arjun Verma', 'arjun.verma@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00011', 'Lucknow', 'customer'),
    ('Meera Kulkarni', 'meera.kulkarni@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00012', 'Nagpur', 'customer'),
    ('Vihaan Singh', 'vihaan.singh@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00013', 'Noida', 'customer'),
    ('Tara Menon', 'tara.menon@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00014', 'Chennai', 'customer'),
    ('Kabir Sethi', 'kabir.sethi@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00015', 'Gurugram', 'customer'),
    ('Aisha Khan', 'aisha.khan@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00016', 'Bhopal', 'customer'),
    ('Nikhil Desai', 'nikhil.desai@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00017', 'Surat', 'customer'),
    ('Riya Chatterjee', 'riya.chatterjee@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00018', 'Bhubaneswar', 'customer'),
    ('Yash Thakur', 'yash.thakur@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00019', 'Dehradun', 'customer'),
    ('Ira Bhatia', 'ira.bhatia@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00020', 'Amritsar', 'customer'),
    ('Manav Gupta', 'manav.gupta@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00021', 'Indore', 'customer'),
    ('Naina Roy', 'naina.roy@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00022', 'Patna', 'customer'),
    ('Rudra Bose', 'rudra.bose@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00023', 'Ranchi', 'customer'),
    ('Sara Thomas', 'sara.thomas@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00024', 'Mangaluru', 'customer'),
    ('Om Prakash', 'om.prakash@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00025', 'Varanasi', 'customer'),
    ('Ishita Jain', 'ishita.jain@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00026', 'Udaipur', 'customer'),
    ('Reyansh Das', 'reyansh.das@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00027', 'Guwahati', 'customer'),
    ('Aditi Narang', 'aditi.narang@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00028', 'Ludhiana', 'customer'),
    ('Karan Arora', 'karan.arora@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00029', 'Faridabad', 'customer'),
    ('Zoya Mirza', 'zoya.mirza@example.com', 'scrypt:32768:8:1$9Le35Cgc7AX7VcMn$f63193ffe5ece93003f9b49a1dec42982b10c558f0df10beed42be11d7528c4e38b72e4e17bab69e059ae168ab70292041e010740b58f9aa4400b880d10bcc2d', '+91 98765 00030', 'Srinagar', 'customer');

INSERT OR IGNORE INTO categories (name, slug, description) VALUES
    ('Electronics', 'electronics', 'Smart devices, accessories, and everyday tech.'),
    ('Fashion', 'fashion', 'Current fits and timeless wardrobe essentials.'),
    ('Books', 'books', 'Ideas, stories, and new perspectives for every reader.'),
    ('Home Appliances', 'home-appliances', 'Thoughtful upgrades for a better home.'),
    ('Beauty', 'beauty', 'Simple, considered self-care essentials.'),
    ('Sports & Fitness', 'sports-fitness', 'Equipment for movement, training, and recovery.'),
    ('Grocery', 'grocery', 'Everyday pantry and kitchen picks.'),
    ('Gaming', 'gaming', 'Gear for play, focus, and competition.'),
    ('Travel', 'travel', 'Useful companions for your next journey.'),
    ('Office', 'office', 'Tools for focused work and study.');

WITH variants(name, slug, offset, image_url) AS (
    VALUES
      ('Pro Essentials', 'pro-essentials', 0, 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&q=80'),
      ('Everyday Kit', 'everyday-kit', 1200, 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&q=80'),
      ('Studio Edition', 'studio-edition', 2400, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&q=80'),
      ('Travel Select', 'travel-select', 800, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&q=80'),
      ('Smart Choice', 'smart-choice', 1700, 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800&q=80'),
      ('Signature Series', 'signature-series', 3200, 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=800&q=80')
)
INSERT OR IGNORE INTO products
    (category_id, name, slug, description, price, original_price, rating, review_count, stock, image_url, featured)
SELECT
    c.id,
    c.name || ' ' || v.name,
    c.slug || '-' || v.slug,
    'A carefully selected ' || lower(c.name) || ' essential from the IntelliCart collection, chosen for quality, value, and everyday usefulness.',
    1299 + c.id * 380 + v.offset,
    1699 + c.id * 460 + v.offset,
    ROUND(4.0 + ((c.id + length(v.name)) % 10) / 10.0, 1),
    24 + ((c.id * 11 + length(v.name)) % 150),
    42 + ((c.id * 17 + v.offset) % 100),
    v.image_url,
    CASE WHEN c.id <= 4 OR v.offset = 0 THEN 1 ELSE 0 END
FROM categories c CROSS JOIN variants v;

WITH RECURSIVE order_seed(id) AS (
    SELECT 1 UNION ALL SELECT id + 1 FROM order_seed WHERE id < 120
)
INSERT OR IGNORE INTO orders
    (customer_id, total_amount, status, payment_status, shipping_address, created_at)
SELECT
    ((id - 1) % 29) + 2,
    0,
    CASE id % 5 WHEN 0 THEN 'delivered' WHEN 1 THEN 'shipped' WHEN 2 THEN 'processing' WHEN 3 THEN 'delivered' ELSE 'delivered' END,
    CASE id % 5 WHEN 2 THEN 'pending' ELSE 'paid' END,
    printf('%d, IntelliCart Avenue, %s, India', 10 + (id % 90), CASE id % 5 WHEN 0 THEN 'Mumbai' WHEN 1 THEN 'Pune' WHEN 2 THEN 'Bengaluru' WHEN 3 THEN 'Delhi' ELSE 'Hyderabad' END),
    datetime('now', printf('-%d days', id % 100))
FROM order_seed;

WITH order_products(order_id, product_id, quantity) AS (
    SELECT id, ((id * 7) % 60) + 1, (id % 3) + 1 FROM orders
)
INSERT OR IGNORE INTO order_items (order_id, product_id, quantity, unit_price)
SELECT op.order_id, op.product_id, op.quantity, p.price
FROM order_products op JOIN products p ON p.id = op.product_id;

UPDATE orders
SET total_amount = (
    SELECT ROUND(SUM(quantity * unit_price), 2)
    FROM order_items
    WHERE order_items.order_id = orders.id
);

INSERT OR IGNORE INTO payments (order_id, method, amount, status, transaction_ref, paid_at)
SELECT
    id,
    CASE id % 3 WHEN 0 THEN 'upi' WHEN 1 THEN 'card' ELSE 'cod' END,
    total_amount,
    payment_status,
    'SEED-' || printf('%04d', id),
    CASE WHEN payment_status = 'paid' THEN created_at ELSE NULL END
FROM orders;

INSERT OR IGNORE INTO reviews (customer_id, product_id, rating, comment, created_at)
SELECT
    ((p.id + 3) % 29) + 2,
    p.id,
    4 + (p.id % 2),
    CASE p.id % 4
      WHEN 0 THEN 'Fast delivery and the quality feels excellent.'
      WHEN 1 THEN 'A useful upgrade that looks even better in person.'
      WHEN 2 THEN 'Good value for the price. I would recommend it.'
      ELSE 'The product matched the description and arrived well packed.'
    END,
    datetime('now', printf('-%d days', p.id % 80))
FROM products p
WHERE p.id <= 30;

WITH RECURSIVE event_seed(id) AS (
    SELECT 1 UNION ALL SELECT id + 1 FROM event_seed WHERE id < 300
)
INSERT INTO interactions (customer_id, product_id, interaction_type, created_at)
SELECT
    ((id - 1) % 29) + 2,
    ((id * 11) % 60) + 1,
    CASE id % 4 WHEN 0 THEN 'view' WHEN 1 THEN 'save' WHEN 2 THEN 'cart' ELSE 'view' END,
    datetime('now', printf('-%d days', id % 70))
FROM event_seed;