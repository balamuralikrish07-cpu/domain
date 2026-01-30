# ==============================
# IMPORT REQUIRED LIBRARIES
# ==============================
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import database and models
from database import db, User, Product, Order, Transport


# ==============================
# APP CONFIGURATION
# ==============================
app = Flask(__name__)
CORS(app)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmmarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database with app
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


# ==============================
# USER REGISTRATION
# ==============================
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    user = User(
        name=data["name"],
        mobile=data["mobile"],
        password=data["password"],
        role=data["role"]  # farmer / vendor
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registered Successfully"})


# ==============================
# USER LOGIN
# ==============================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(
        mobile=data["mobile"],
        password=data["password"]
    ).first()

    if user:
        return jsonify({
            "id": user.id,
            "name": user.name,
            "role": user.role
        })

    return jsonify({"message": "Invalid Login"}), 401


# ==============================
# ADD PRODUCT (FARMER)
# ==============================
@app.route("/add-product", methods=["POST"])
def add_product():
    data = request.json

    product = Product(
        farmer_id=data["farmer_id"],
        name=data["name"],
        quantity=data["quantity"],
        price=data["price"],
        location=data["location"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Product Added Successfully"})


# ==============================
# VIEW ALL PRODUCTS (VENDOR)
# ==============================
@app.route("/products", methods=["GET"])
def view_products():
    products = Product.query.all()
    result = []

    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price,
            "location": p.location,
            "farmer_id": p.farmer_id
        })

    return jsonify(result)


# ==============================
# PLACE ORDER (VENDOR)
# ==============================
@app.route("/order", methods=["POST"])
def place_order():
    data = request.json

    order = Order(
        product_id=data["product_id"],
        vendor_id=data["vendor_id"],
        quantity=data["quantity"],
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order Placed Successfully"})


# ==============================
# ADD TRANSPORT DETAILS
# ==============================
@app.route("/add-transport", methods=["POST"])
def add_transport():
    data = request.json

    transport = Transport(
        order_id=data["order_id"],
        vehicle=data["vehicle"],
        driver=data["driver"],
        contact=data["contact"],
        status="On the Way"
    )

    db.session.add(transport)
    db.session.commit()

    return jsonify({"message": "Transport Assigned Successfully"})


# ==============================
# VIEW ALL ORDERS
# ==============================
@app.route("/orders", methods=["GET"])
def view_orders():
    orders = Order.query.all()
    result = []

    for o in orders:
        result.append({
            "id": o.id,
            "product_id": o.product_id,
            "vendor_id": o.vendor_id,
            "quantity": o.quantity,
            "status": o.status
        })

    return jsonify(result)


# ==============================
# START SERVER
# ==============================
if __name__ == "__main__":
    app.run(debug=True)
