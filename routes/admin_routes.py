from flask import Blueprint, jsonify, request
from models import db, Product
from utils.role_required import role_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/products", methods=["POST"])
@role_required("admin")
def create_product():
    # Try parsing JSON safely
    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({"message": "Invalid JSON format", "error": str(e)}), 400

    # Debug check
    if not data:
        return jsonify({"message": "Missing JSON data"}), 400

    # Field validation
    if "name" not in data or "price" not in data:
        return jsonify({"message": "Missing 'name' or 'price' field"}), 400

    try:
        new_product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description"),
            image=data.get("image")
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating product", "error": str(e)}), 500


@admin_bp.route("/products/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200
