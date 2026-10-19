import json, os, uuid
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-publishing")
DATA_FILE = Path(__file__).with_name("products.json")
DATA_FILE.touch(exist_ok=True)
if DATA_FILE.read_text(encoding="utf-8").strip() == "":
    DATA_FILE.write_text("[]", encoding="utf-8")

def get_products():
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_products(products):
    DATA_FILE.write_text(json.dumps(products, indent=2, ensure_ascii=False), encoding="utf-8")

def shop_name():
    return os.environ.get("SHOP_NAME", "FLEX AND FIT")

def whatsapp_numbers():
    numbers = [
        "".join(ch for ch in os.environ.get("WHATSAPP_NUMBER", "254780572505") if ch.isdigit()),
        "".join(ch for ch in os.environ.get("WHATSAPP_NUMBER_2", "254798230681") if ch.isdigit()),
    ]
    return [number for number in numbers if number]

def admin_required():
    return session.get("admin") is True

@app.route("/")
def index():
    products = get_products()
    q = request.args.get("q", "").strip().lower()
    category = request.args.get("category", "").strip()
    if q:
        products = [p for p in products if q in p["name"].lower() or q in p.get("description", "").lower()]
    if category:
        products = [p for p in products if p.get("category") == category]
    categories = ["Clothes", "Shoes", "Bags", "Accessories"]
    return render_template("index.html", products=products, q=q, category=category,
                           categories=categories, shop_name=shop_name(), whatsapp_numbers=whatsapp_numbers())

@app.route("/product/<product_id>")
def product(product_id):
    item = next((p for p in get_products() if p["id"] == product_id), None)
    if item is None:
        abort(404)
    return render_template("product.html", item=item, shop_name=shop_name(), whatsapp_numbers=whatsapp_numbers())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST" and not admin_required():
        if request.form.get("password", "") == os.environ.get("ADMIN_PASSWORD", "change-me"):
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("That password did not match.")
    if not admin_required():
        return render_template("login.html", shop_name=shop_name())
    return render_template("admin.html", products=get_products(), shop_name=shop_name())

@app.route("/admin/add", methods=["POST"])
def add_product():
    if not admin_required():
        abort(403)
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    image_url = request.form.get("image_url", "").strip()
    category = request.form.get("category", "Clothes")
    sizes = request.form.get("sizes", "").strip()
    try:
        price = float(request.form.get("price", ""))
        if price < 0: raise ValueError
    except ValueError:
        flash("Enter a valid non-negative price.")
        return redirect(url_for("admin"))
    if not name:
        flash("Please enter a product name.")
        return redirect(url_for("admin"))
    products = get_products()
    products.insert(0, {"id": uuid.uuid4().hex[:10], "name": name, "price": price,
                        "description": description, "image_url": image_url,
                        "category": category, "sizes": sizes})
    save_products(products)
    flash("Product added to your shop.")
    return redirect(url_for("admin"))

@app.route("/admin/delete/<product_id>", methods=["POST"])
def delete_product(product_id):
    if not admin_required():
        abort(403)
    save_products([p for p in get_products() if p["id"] != product_id])
    flash("Product removed.")
    return redirect(url_for("admin"))

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)
