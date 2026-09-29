from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.product_variant import ProductVariant

product_variants_bp = Blueprint("product_variants", __name__, url_prefix="/api/product-variants")


@product_variants_bp.route("", methods=["GET"])
def get_product_variants():
    """Return every product variant in the database as JSON."""
    variants = ProductVariant.query.all()
    return jsonify([v.to_dict() for v in variants]), 200


@product_variants_bp.route("/<int:variant_id>", methods=["GET"])
def get_product_variant(variant_id):
    """Return a single product variant by its ID, or 404 if it doesn't exist."""
    variant = ProductVariant.query.get_or_404(variant_id)
    return jsonify(variant.to_dict()), 200


@product_variants_bp.route("", methods=["POST"])
def create_product_variant():
    """Create a new variant. Body: {product_id, color, size, buying_price, selling_price, quantity_on_hand, reorder_level}"""
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    buying_price = data.get("buying_price")
    selling_price = data.get("selling_price")

    if not product_id or buying_price is None or selling_price is None:
        return jsonify({"error": "product_id, buying_price, and selling_price are required"}), 400

    new_variant = ProductVariant(
        product_id=product_id,
        color=data.get("color"),
        size=data.get("size"),
        buying_price=buying_price,
        selling_price=selling_price,
        quantity_on_hand=data.get("quantity_on_hand", 0),
        reorder_level=data.get("reorder_level", 0),
    )
    db.session.add(new_variant)
    db.session.commit()

    return jsonify(new_variant.to_dict()), 201