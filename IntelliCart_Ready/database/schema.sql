PRAGMA foreign_keys = ON;
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100) NOT NULL, email VARCHAR(150) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL, segment VARCHAR(30) DEFAULT 'New Customer', created_at DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE products (id INTEGER PRIMARY KEY, name VARCHAR(150) NOT NULL, category VARCHAR(50) NOT NULL, price DECIMAL(10,2) NOT NULL CHECK(price>=0), rating DECIMAL(2,1) NOT NULL CHECK(rating BETWEEN 0 AND 5), stock INTEGER NOT NULL CHECK(stock>=0), description TEXT, image TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, total DECIMAL(12,2) NOT NULL CHECK(total>=0), status VARCHAR(30) DEFAULT 'Placed', created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id));
CREATE TABLE order_items (id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL CHECK(quantity>0), price DECIMAL(10,2) NOT NULL CHECK(price>=0), FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE, FOREIGN KEY(product_id) REFERENCES products(id));
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
