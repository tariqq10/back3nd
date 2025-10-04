from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

# Enable CORS (important for React frontend)
CORS(app)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["JWT_SECRET_KEY"] = "supersecretkey"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# Initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(product_bp)
app.register_blueprint(order_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# Create tables + seed admin
with app.app_context():
    db.create_all()
    from models import User
    if not User.query.filter_by(username="admin").first():
        from flask_bcrypt import generate_password_hash
        admin_user = User(
            username="admin",
            password=generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin seeded: username=admin, password=admin123")

if __name__ == "__main__":
    app.run(debug=True)
