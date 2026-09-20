from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from src.extensions import db
from src.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Create a new user. Body: {first_name, last_name, email, password, role_id, business_id}"""
    data = request.get_json(silent=True) or {}

    first_name = data.get("first_name")
    last_name= data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    role_id = data.get("role_id")
    business_id = data.get("business_id")

    if not all([first_name, last_name, email, password, role_id, business_id]):
        return jsonify({"error": "first_name, last_name, email, password, role_id, and business_id are all required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "A user with this email already exists"}), 409

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        role_id=role_id,
        business_id=business_id,
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Verify credentials and return a JWT. Body: {email, password}"""
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.user_id))

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict(),
    }), 200