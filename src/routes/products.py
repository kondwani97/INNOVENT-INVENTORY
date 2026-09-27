from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.product import Product

products_bp = Blueprint("products", __name__, url_prefix="/api/products")


@products_bp.route("", methods=["GET"])
def get_products():
    """Return every product in the database as JSON."""
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products]), 200


@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Return a single product by its ID, or 404 if it doesn't exist."""
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200


@products_bp.route("", methods=["POST"])
def create_product():
    """Create a new product. Body: {name, description, category_id, supplier_id, image_url, status}"""
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    category_id = data.get("category_id")

    if not name or not category_id:
        return jsonify({"error": "name and category_id are required"}), 400

    new_product = Product(
        name=name,
        description=data.get("description"),
        category_id=category_id,
        supplier_id=data.get("supplier_id"),
        image_url=data.get("image_url"),
        status=data.get("status", "active"),
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.to_dict()), 201