from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.category import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.route("", methods=["GET"])
def get_categories():
    """Return every category in the database as JSON."""
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories]), 200


@categories_bp.route("/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """Return a single category by its ID, or 404 if it doesn't exist."""
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200


@categories_bp.route("", methods=["POST"])
def create_category():
    """Create a new category from JSON body: {"name": "Beverages", "description": "..."}"""
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    description = data.get("description")

    if not name:
        return jsonify({"error": "name is required"}), 400

    new_category = Category(name=name, description=description)
    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category.to_dict()), 201