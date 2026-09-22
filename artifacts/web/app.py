import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from ml.customer_segmentation import segment_customers
from ml.recommendation import recommend_for_customer, recommend_similar


BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "intellicart.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
DATA_PATH = DATABASE_DIR / "data.sql"
TRIGGERS_PATH = DATABASE_DIR / "triggers.sql"
VIEWS_PATH = DATABASE_DIR / "views.sql"

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", secrets.token_hex(32))
app.config["DATABASE"] = str(DATABASE_PATH)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_database():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    first_run = not DATABASE_PATH.exists()
    with app.app_context():
        db = get_db()
        db.executescript(SCHEMA_PATH.read_text())
        db.executescript(TRIGGERS_PATH.read_text())
        db.executescript(VIEWS_PATH.read_text())
        customer_count = db.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        if first_run or customer_count == 0:
            db.executescript(DATA_PATH.read_text())
        db.commit()


def query_db(query, args=(), one=False):
    cursor = get_db().execute(query, args)
    rows = cursor.fetchall()
    cursor.close()
    return (rows[0] if rows else None) if one else rows


def execute_db(query, args=()):
    db = get_db()
    cursor = db.execute(query, args)
    db.commit()
    return cursor


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Please sign in to continue.", "info")
            return redirect(url_for("login", next=request.path))
        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        user = get_current_user()
        if not user or user["role"] != "admin":
            flash("Admin access is required for that page.", "error")
            return redirect(url_for("home"))
        return view(**kwargs)

    return wrapped_view


def get_current_user():
    if "user_id" not in session:
        return None
    return query_db(
        "SELECT * FROM customers WHERE id = ?", (session["user_id"],), one=True
    )


def cart_items():
    cart = session.get("cart", {})
    if not cart:
        return []
    product_ids = [int(product_id) for product_id in cart]
    placeholders = ",".join("?" for _ in product_ids)
    products = query_db(
        f"""
        SELECT p.*, c.name AS category_name
        FROM products p
        JOIN categories c ON c.id = p.category_id
        WHERE p.id IN ({placeholders})
        """,
        product_ids,
    )
    items = []
    for product in products:
        quantity = max(1, int(cart.get(str(product["id"]), 1)))
        items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": product["price"] * quantity,
            }
        )
    return items


def cart_totals():
    items = cart_items()
    subtotal = sum(item["subtotal"] for item in items)
    discount = round(subtotal * 0.1, 2) if subtotal >= 5000 else 0
    return items, subtotal, discount, round(subtotal - discount, 2)


@app.context_processor
def inject_layout_data():
    user = get_current_user()
    cart = session.get("cart", {})
    return {
        "current_user": user,
        "cart_count": sum(int(value) for value in cart.values()),
        "current_path": request.path,
    }


@app.get("/")
def home():
    featured = query_db(
        """
        SELECT p.*, c.name AS category_name
        FROM products p JOIN categories c ON c.id = p.category_id
        WHERE p.featured = 1 ORDER BY p.rating DESC LIMIT 4
        """
    )
    trending = query_db(
        """
        SELECT p.*, c.name AS category_name, COUNT(i.id) AS interaction_count
        FROM products p
        JOIN categories c ON c.id = p.category_id
        LEFT JOIN interactions i ON i.product_id = p.id
        GROUP BY p.id ORDER BY interaction_count DESC, p.rating DESC LIMIT 4
        """
    )
    categories = query_db(
        "SELECT c.*, COUNT(p.id) AS product_count FROM categories c LEFT JOIN products p ON p.category_id = c.id GROUP BY c.id ORDER BY c.name"
    )
    stats = {
        "products": query_db("SELECT COUNT(*) AS count FROM products", one=True)["count"],
        "customers": query_db("SELECT COUNT(*) AS count FROM customers", one=True)["count"],
        "orders": query_db("SELECT COUNT(*) AS count FROM orders", one=True)["count"],
        "satisfaction": query_db("SELECT ROUND(AVG(rating) * 20, 0) AS score FROM reviews", one=True)["score"] or 98,
    }
    return render_template(
        "index.html",
        featured=featured,
        trending=trending,
        categories=categories,
        stats=stats,
    )


@app.get("/products")
def products():
    search = request.args.get("search", "").strip()
    category_id = request.args.get("category", type=int)
    min_rating = request.args.get("rating", type=float)
    max_price = request.args.get("max_price", type=float)
    sort = request.args.get("sort", "popular")
    conditions = ["1 = 1"]
    args = []
    if search:
        conditions.append("(p.name LIKE ? OR p.description LIKE ? OR c.name LIKE ?)")
        search_value = f"%{search}%"
        args.extend([search_value, search_value, search_value])
    if category_id:
        conditions.append("p.category_id = ?")
        args.append(category_id)
    if min_rating:
        conditions.append("p.rating >= ?")
        args.append(min_rating)
    if max_price:
        conditions.append("p.price <= ?")
        args.append(max_price)
    sort_sql = {
        "price_low": "p.price ASC",
        "price_high": "p.price DESC",
        "rating": "p.rating DESC",
        "popular": "p.review_count DESC, p.rating DESC",
    }.get(sort, "p.review_count DESC, p.rating DESC")
    product_rows = query_db(
        f"""
        SELECT p.*, c.name AS category_name
        FROM products p JOIN categories c ON c.id = p.category_id
        WHERE {" AND ".join(conditions)}
        ORDER BY {sort_sql}
        """,
        args,
    )
    return render_template(
        "products.html",
        products=product_rows,
        categories=query_db("SELECT * FROM categories ORDER BY name"),
        filters={
            "search": search,
            "category": category_id,
            "rating": min_rating,
            "max_price": max_price,
            "sort": sort,
        },
    )


@app.get("/product/<int:product_id>")
def product_detail(product_id):
    product = query_db(
        """
        SELECT p.*, c.name AS category_name, c.slug AS category_slug
        FROM products p JOIN categories c ON c.id = p.category_id
        WHERE p.id = ?
        """,
        (product_id,),
        one=True,
    )
    if not product:
        return render_template("not_found.html"), 404
    reviews = query_db(
        """
        SELECT r.*, c.name AS customer_name FROM reviews r
        JOIN customers c ON c.id = r.customer_id
        WHERE r.product_id = ? ORDER BY r.created_at DESC LIMIT 4
        """,
        (product_id,),
    )
    recommendations = recommend_similar(get_db(), product_id, limit=4)
    if get_current_user():
        execute_db(
            "INSERT INTO interactions (customer_id, product_id, interaction_type) VALUES (?, ?, ?)",
            (get_current_user()["id"], product_id, "view"),
        )
    return render_template(
        "product_detail.html",
        product=product,
        reviews=reviews,
        recommendations=recommendations,
    )


@app.get("/recommendations")
def recommendations():
    user = get_current_user()
    recommended = (
        recommend_for_customer(get_db(), user["id"], limit=8)
        if user
        else query_db(
            """
            SELECT p.*, c.name AS category_name FROM products p
            JOIN categories c ON c.id = p.category_id
            ORDER BY p.rating DESC, p.review_count DESC LIMIT 8
            """
        )
    )
    return render_template("recommendations.html", recommendations=recommended, personalized=bool(user))


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = query_db("SELECT * FROM customers WHERE email = ?", (email,), one=True)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Email or password is incorrect.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            session["cart"] = {}
            next_url = request.args.get("next") or request.form.get("next") or url_for("home")
            return redirect(next_url)
    return render_template("auth.html", mode="login")


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()
        city = request.form.get("city", "").strip()
        if not name or not email or len(password) < 6:
            flash("Add your name, a valid email, and a password with at least 6 characters.", "error")
        elif query_db("SELECT id FROM customers WHERE email = ?", (email,), one=True):
            flash("An account with that email already exists.", "error")
        else:
            cursor = execute_db(
                """
                INSERT INTO customers (name, email, password_hash, phone, city, role)
                VALUES (?, ?, ?, ?, ?, 'customer')
                """,
                (name, email, generate_password_hash(password), phone, city),
            )
            session.clear()
            session["user_id"] = cursor.lastrowid
            session["cart"] = {}
            flash("Welcome to IntelliCart.", "success")
            return redirect(url_for("home"))
    return render_template("auth.html", mode="register")


@app.get("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("home"))


@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = query_db("SELECT id, name, stock FROM products WHERE id = ?", (product_id,), one=True)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    cart = session.setdefault("cart", {})
    current_quantity = int(cart.get(str(product_id), 0))
    cart[str(product_id)] = min(current_quantity + request.form.get("quantity", 1, type=int), product["stock"])
    session.modified = True
    if get_current_user():
        execute_db(
            "INSERT INTO interactions (customer_id, product_id, interaction_type) VALUES (?, ?, ?)",
            (get_current_user()["id"], product_id, "cart"),
        )
    flash(f"{product['name']} was added to your cart.", "success")
    return redirect(request.referrer or url_for("products"))


@app.post("/cart/update")
def update_cart():
    cart = session.setdefault("cart", {})
    for product_id, quantity in request.form.items():
        if not product_id.isdigit():
            continue
        product = query_db("SELECT stock FROM products WHERE id = ?", (int(product_id),), one=True)
        if not product:
            cart.pop(product_id, None)
            continue
        quantity_value = max(0, min(int(quantity or 0), product["stock"]))
        if quantity_value == 0:
            cart.pop(product_id, None)
        else:
            cart[product_id] = quantity_value
    session.modified = True
    flash("Your cart was updated.", "success")
    return redirect(url_for("cart"))


@app.post("/cart/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.setdefault("cart", {})
    cart.pop(str(product_id), None)
    session.modified = True
    flash("Item removed from your cart.", "info")
    return redirect(url_for("cart"))


@app.get("/cart")
def cart():
    items, subtotal, discount, total = cart_totals()
    return render_template(
        "cart.html",
        items=items,
        subtotal=subtotal,
        discount=discount,
        total=total,
    )


@app.route("/checkout", methods=("GET", "POST"))
@login_required
def checkout():
    items, subtotal, discount, total = cart_totals()
    if not items:
        flash("Add an item to your cart before checking out.", "info")
        return redirect(url_for("products"))
    if request.method == "POST":
        address = request.form.get("address", "").strip()
        payment_method = request.form.get("payment_method", "cod")
        if not address:
            flash("Please enter a delivery address.", "error")
        else:
            db = get_db()
            try:
                cursor = db.execute(
                    """
                    INSERT INTO orders (customer_id, total_amount, status, payment_status, shipping_address)
                    VALUES (?, ?, 'processing', ?, ?)
                    """,
                    (session["user_id"], total, "paid" if payment_method != "cod" else "pending", address),
                )
                order_id = cursor.lastrowid
                for item in items:
                    stock = query_db("SELECT stock FROM products WHERE id = ?", (item["product"]["id"],), one=True)["stock"]
                    if stock < item["quantity"]:
                        raise ValueError(f"{item['product']['name']} no longer has enough stock.")
                    db.execute(
                        "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
                        (order_id, item["product"]["id"], item["quantity"], item["product"]["price"]),
                    )
                db.execute(
                    """
                    INSERT INTO payments (order_id, method, amount, status, transaction_ref)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (order_id, payment_method, total, "paid" if payment_method != "cod" else "pending", f"IC-{secrets.token_hex(4).upper()}"),
                )
                db.commit()
                session["cart"] = {}
                return redirect(url_for("order_success", order_id=order_id))
            except (sqlite3.Error, ValueError) as error:
                db.rollback()
                flash(str(error), "error")
    return render_template(
        "checkout.html",
        items=items,
        subtotal=subtotal,
        discount=discount,
        total=total,
    )


@app.get("/order-success/<int:order_id>")
@login_required
def order_success(order_id):
    order = query_db(
        """
        SELECT o.*, p.method, p.status AS payment_state
        FROM orders o LEFT JOIN payments p ON p.order_id = o.id
        WHERE o.id = ? AND o.customer_id = ?
        """,
        (order_id, session["user_id"]),
        one=True,
    )
    if not order:
        return render_template("not_found.html"), 404
    return render_template("order_success.html", order=order)


@app.get("/orders")
@login_required
def orders():
    order_rows = query_db(
        """
        SELECT o.*, GROUP_CONCAT(p.name, ', ') AS products
        FROM orders o
        LEFT JOIN order_items oi ON oi.order_id = o.id
        LEFT JOIN products p ON p.id = oi.product_id
        WHERE o.customer_id = ?
        GROUP BY o.id ORDER BY o.created_at DESC
        """,
        (session["user_id"],),
    )
    return render_template("orders.html", orders=order_rows)


@app.get("/profile")
@login_required
def profile():
    user = get_current_user()
    summary = query_db(
        """
        SELECT COUNT(*) AS orders, COALESCE(SUM(total_amount), 0) AS spent
        FROM orders WHERE customer_id = ?
        """,
        (user["id"],),
        one=True,
    )
    return render_template("profile.html", user=user, summary=summary)


@app.get("/admin")
@admin_required
def admin():
    stats = query_db("SELECT * FROM dashboard_summary", one=True)
    monthly_sales = query_db("SELECT * FROM monthly_sales ORDER BY month")
    category_sales = query_db("SELECT * FROM category_sales ORDER BY revenue DESC")
    top_products = query_db("SELECT * FROM top_products ORDER BY units_sold DESC LIMIT 10")
    recent_orders = query_db(
        """
        SELECT o.*, c.name AS customer_name FROM orders o
        JOIN customers c ON c.id = o.customer_id
        ORDER BY o.created_at DESC LIMIT 8
        """
    )
    top_customers = query_db(
        """
        SELECT c.name, c.city, COUNT(o.id) AS orders, COALESCE(SUM(o.total_amount), 0) AS spent
        FROM customers c JOIN orders o ON o.customer_id = c.id
        GROUP BY c.id ORDER BY spent DESC LIMIT 6
        """
    )
    low_stock = query_db(
        """
        SELECT p.*, c.name AS category_name FROM products p
        JOIN categories c ON c.id = p.category_id WHERE p.stock < 35
        ORDER BY p.stock LIMIT 8
        """
    )
    segments = segment_customers(get_db())
    return render_template(
        "admin.html",
        stats=stats,
        monthly_sales=monthly_sales,
        category_sales=category_sales,
        top_products=top_products,
        recent_orders=recent_orders,
        top_customers=top_customers,
        low_stock=low_stock,
        segments=segments,
    )


@app.get("/api/analytics")
@admin_required
def analytics_api():
    return jsonify(
        {
            "monthly_sales": [dict(row) for row in query_db("SELECT * FROM monthly_sales ORDER BY month")],
            "category_sales": [dict(row) for row in query_db("SELECT * FROM category_sales ORDER BY revenue DESC")],
            "segments": segment_customers(get_db()),
        }
    )


@app.get("/healthz")
def health_check():
    return {"status": "ok", "service": "intellicart"}


with app.app_context():
    init_database()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)