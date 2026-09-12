from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.role import Role

roles_bp = Blueprint("roles", __name__, url_prefix="/api/roles")


@roles_bp.route("", methods=["GET"])
def get_roles():
    """Return every role in the database as JSON."""
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200


@roles_bp.route("/<int:role_id>", methods=["GET"])
def get_role(role_id):
    """Return a single role by its ID, or 404 if it doesn't exist."""
    role = Role.query.get_or_404(role_id)
    return jsonify(role.to_dict()), 200


@roles_bp.route("", methods=["POST"])
def create_role():
    """Create a new role from JSON body: {"role_name": "Manager"}"""
    data = request.get_json(silent=True) or {}
    role_name = data.get("role_name")

    if not role_name:
        return jsonify({"error": "role_name is required"}), 400

    new_role = Role(role_name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return jsonify(new_role.to_dict()), 201
