from flask import Blueprint, jsonify, request
from models import db, Product
from utils.role_required import role_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/products", methods=["POST"])
@role_required("admin")
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data["name"],
        price=data["price"],
        description=data.get("description"),
        image=data.get("image")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

@admin_bp.route("/products/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
