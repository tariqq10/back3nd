from flask import Blueprint, jsonify
from models import Product

product_bp = Blueprint("products", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "image": p.image
        } for p in products
    ])
