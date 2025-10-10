from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
from utils.extensions import bcrypt

auth_bp = Blueprint("auth", __name__)

# Register endpoint
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    # ✅ Use bcrypt for hashing consistently
    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# Login endpoint
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ Create JWT token with role info
    access_token = create_access_token(
        identity={"id": user.id, "username": user.username, "role": user.role}
    )

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "role": user.role
    }), 200