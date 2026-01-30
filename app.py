from flask import Flask, request, jsonify
from flask_cors import CORS

from database import db, User, Product, Order, Transport



app = Flask(__name__)
CORS(app, resources={r"/": {"origins": ""}})

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///farmmarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Connect DB
db.init_app(app)

({            "id": p.id,
            "name": p.name,
            "quantity": p.quantity,
            "price": p.price,
            "location": p.location,
            "farmer_id": p.farmer_id
        })

    return jsonify(result)



@app.route("/order", methods=["POST"])
def order():

    data = request.json

    order = Order(
        product_id=data["product_id"],
        vendor_id=data["vendor_id"],
        quantity=data["quantity"],
        status="Pending"
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Order Placed"})



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

    return jsonify({"message": "Transport Assigned"})



@app.route("/orders")
def orders():

    result = []

    for o in Order.query.all():
        result.append({
            "id": o.id,
            "product_id": o.product_id,
            "vendor_id": o.vendor_id,
            "quantity": o.quantity,
            "status": o.status
        })

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)
