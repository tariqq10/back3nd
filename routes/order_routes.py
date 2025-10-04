from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint("orders", __name__)

@order_bp.route("/orders", methods=["POST"])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    if current_user["role"] != "buyer":
        return jsonify({"message": "Only buyers can place orders"}), 403

    data = request.get_json()
    print("🛒 Order placed by:", current_user["id"], data)
    return jsonify({"message": "Order created successfully"}), 201
