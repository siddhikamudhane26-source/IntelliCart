import os, sqlite3, secrets, random
from pathlib import Path
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

BASE = Path(__file__).resolve().parent
DB = BASE / "database" / "intellicart.db"
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "intellicart-demo-secret")

CATEGORIES = ["Electronics","Fashion","Home","Beauty","Sports","Books","Grocery","Accessories"]
ADJECTIVES = ["Smart","Premium","Classic","Modern","Essential","Pro","Ultra","Eco","Urban","Daily"]
NOUNS = ["Headphones","Backpack","Watch","Lamp","Shoes","Keyboard","Bottle","Camera","T-Shirt","Speaker",
         "Notebook","Mouse","Skincare Kit","Coffee Maker","Yoga Mat","Power Bank","Sunglasses","Chair","Tablet","Perfume"]

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    DB.parent.mkdir(exist_ok=True)
    con = db()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL, segment TEXT DEFAULT 'New Customer', created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS products(
      id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, price REAL NOT NULL,
      rating REAL NOT NULL, stock INTEGER NOT NULL, description TEXT, image TEXT
    );
    CREATE TABLE IF NOT EXISTS orders(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, total REAL, status TEXT DEFAULT 'Placed',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS order_items(
      id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, product_id INTEGER, quantity INTEGER,
      price REAL, FOREIGN KEY(order_id) REFERENCES orders(id), FOREIGN KEY(product_id) REFERENCES products(id)
    );
    """)
    count = con.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count < 500:
        con.execute("DELETE FROM products")
        random.seed(42)
        rows=[]
        for i in range(1,501):
            cat=CATEGORIES[(i-1)%len(CATEGORIES)]
            name=f"{ADJECTIVES[(i*3)%len(ADJECTIVES)]} {NOUNS[(i*7)%len(NOUNS)]} {i}"
            price=round(random.uniform(199, 24999),2)
            rating=round(random.uniform(3.2,5.0),1)
            stock=random.randint(5,120)
            desc=f"High-quality {cat.lower()} product with reliable performance, modern design and excellent value."
            image=f"https://images.unsplash.com/photo-{['1498049794561-7780e7231661','1523275335684-37898b6baf30','1542291026-7eec264c27ff','1505740420928-5e560c06d30e'][i%4]}?auto=format&fit=crop&w=800&q=80"
            rows.append((i,name,cat,price,rating,stock,desc,image))
        con.executemany("INSERT INTO products VALUES(?,?,?,?,?,?,?,?)",rows)
    con.commit(); con.close()

def login_required(fn):
    @wraps(fn)
    def wrapper(*a,**kw):
        if "user_id" not in session:
            flash("Please login first.","warning")
            return redirect(url_for("login", next=request.path))
        return fn(*a,**kw)
    return wrapper

def cart_items():
    cart=session.get("cart",{})
    if not cart: return [],0
    con=db()
    ids=[int(x) for x in cart]
    q="SELECT * FROM products WHERE id IN (%s)" % ",".join("?"*len(ids))
    rows=con.execute(q,ids).fetchall(); con.close()
    items=[]; total=0
    for p in rows:
        qty=int(cart[str(p["id"])])
        subtotal=p["price"]*qty; total+=subtotal
        items.append({"p":p,"qty":qty,"subtotal":subtotal})
    return items,total

@app.context_processor
def globals():
    return {"cart_count":sum(session.get("cart",{}).values())}

@app.route("/")
def home():
    con=db()
    featured=con.execute("SELECT * FROM products ORDER BY rating DESC, id LIMIT 8").fetchall()
    cats=[{"name":c,"count":con.execute("SELECT COUNT(*) FROM products WHERE category=?",(c,)).fetchone()[0]} for c in CATEGORIES]
    stats={"products":con.execute("SELECT COUNT(*) FROM products").fetchone()[0],
           "customers":con.execute("SELECT COUNT(*) FROM users").fetchone()[0],
           "orders":con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]}
    con.close()
    return render_template("home.html",featured=featured,cats=cats,stats=stats)

@app.route("/products")
def products():
    con=db(); search=request.args.get("q","").strip(); category=request.args.get("category","")
    sort=request.args.get("sort","featured")
    sql="SELECT * FROM products WHERE 1=1"; args=[]
    if search: sql+=" AND (name LIKE ? OR description LIKE ?)"; args += [f"%{search}%",f"%{search}%"]
    if category: sql+=" AND category=?"; args.append(category)
    if sort=="price_low": sql+=" ORDER BY price ASC"
    elif sort=="price_high": sql+=" ORDER BY price DESC"
    elif sort=="rating": sql+=" ORDER BY rating DESC"
    else: sql+=" ORDER BY rating DESC, id DESC"
    rows=con.execute(sql,args).fetchall(); con.close()
    return render_template("products.html",products=rows,categories=CATEGORIES,search=search,category=category,sort=sort)

@app.route("/product/<int:pid>")
def product(pid):
    con=db(); p=con.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()
    related=con.execute("SELECT * FROM products WHERE category=? AND id!=? ORDER BY rating DESC LIMIT 4",(p["category"],pid)).fetchall() if p else []
    con.close()
    if not p: return "Product not found",404
    return render_template("product.html",p=p,related=related)

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form["name"].strip(); email=request.form["email"].strip().lower(); password=request.form["password"]
        con=db()
        try:
            con.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",(name,email,password)); con.commit()
            flash("Account created. Please login.","success"); return redirect(url_for("login"))
        except sqlite3.IntegrityError: flash("Email already registered.","danger")
        finally: con.close()
    return render_template("auth.html",mode="register")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"].strip().lower(); password=request.form["password"]
        con=db(); u=con.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password)).fetchone(); con.close()
        if u:
            session["user_id"]=u["id"]; session["user_name"]=u["name"]; return redirect(request.args.get("next") or url_for("home"))
        flash("Invalid email or password.","danger")
    return render_template("auth.html",mode="login")

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("home"))

@app.route("/cart/add/<int:pid>",methods=["POST"])
def add_cart(pid):
    cart=session.setdefault("cart",{}); key=str(pid); cart[key]=int(cart.get(key,0))+1
    session.modified=True; flash("Added to cart.","success"); return redirect(request.referrer or url_for("products"))

@app.route("/cart",methods=["GET","POST"])
def cart():
    if request.method=="POST":
        for k,v in request.form.items():
            if k.startswith("qty_"):
                pid=k[4:]
                try: session["cart"][pid]=max(0,int(v))
                except: pass
        session["cart"]={k:v for k,v in session.get("cart",{}).items() if v>0}; session.modified=True
        return redirect(url_for("cart"))
    items,total=cart_items(); return render_template("cart.html",items=items,total=total)

@app.route("/cart/remove/<int:pid>")
def remove_cart(pid):
    session.get("cart",{}).pop(str(pid),None); session.modified=True; return redirect(url_for("cart"))

@app.route("/checkout",methods=["GET","POST"])
@login_required
def checkout():
    items,total=cart_items()
    if not items: return redirect(url_for("products"))
    if request.method=="POST":
        con=db(); oid=con.execute("INSERT INTO orders(user_id,total) VALUES(?,?)",(session["user_id"],total)).lastrowid
        for it in items:
            con.execute("INSERT INTO order_items(order_id,product_id,quantity,price) VALUES(?,?,?,?)",(oid,it["p"]["id"],it["qty"],it["p"]["price"]))
        con.commit(); con.close(); session["cart"]={}; return redirect(url_for("success",oid=oid))
    return render_template("checkout.html",items=items,total=total)

@app.route("/order-success/<int:oid>")
@login_required
def success(oid): return render_template("success.html",oid=oid)

@app.route("/orders")
@login_required
def orders():
    con=db(); rows=con.execute("SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",(session["user_id"],)).fetchall(); con.close()
    return render_template("orders.html",orders=rows)

@app.route("/recommendations")
@login_required
def recommendations():
    con=db()
    u=con.execute("SELECT * FROM users WHERE id=?",(session["user_id"],)).fetchone()
    rows=con.execute("SELECT * FROM products ORDER BY rating DESC LIMIT 12").fetchall()
    con.close(); return render_template("recommendations.html",products=rows,user=u)

@app.route("/admin")
def admin():
    con=db()
    stats={"products":con.execute("SELECT COUNT(*) FROM products").fetchone()[0],
           "users":con.execute("SELECT COUNT(*) FROM users").fetchone()[0],
           "orders":con.execute("SELECT COUNT(*) FROM orders").fetchone()[0],
           "revenue":con.execute("SELECT COALESCE(SUM(total),0) FROM orders").fetchone()[0]}
    top=con.execute("""SELECT p.name, SUM(oi.quantity) qty FROM order_items oi JOIN products p ON p.id=oi.product_id
                       GROUP BY p.id ORDER BY qty DESC LIMIT 8""").fetchall()
    segments=con.execute("SELECT segment,COUNT(*) count FROM users GROUP BY segment").fetchall()
    con.close(); return render_template("admin.html",stats=stats,top=top,segments=segments)

@app.route("/api/analytics")
def analytics():
    con=db()
    data={"categories":[dict(r) for r in con.execute("SELECT category,COUNT(*) count FROM products GROUP BY category").fetchall()],
          "orders":[dict(r) for r in con.execute("SELECT date(created_at) day,COUNT(*) count FROM orders GROUP BY date(created_at) ORDER BY day").fetchall()]}
    con.close(); return jsonify(data)

@app.route("/healthz")
def healthz(): return {"status":"ok","app":"IntelliCart"}

init_db()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT","5000")))
