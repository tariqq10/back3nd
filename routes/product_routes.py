from flask import Blueprint, jsonify
import json
import os

product_bp = Blueprint("products", __name__)

@product_bp.route("/products", methods=["GET"])
def get_products():
    try:
        # Get absolute path to products.json in the root
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../products.json")
        with open(json_path, "r") as f:
            products = json.load(f)
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"message": "Failed to load products", "error": str(e)}), 500
