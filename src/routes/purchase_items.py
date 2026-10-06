from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.purchase_item import PurchaseItem

purchase_items_bp = Blueprint("purchase_items", __name__, url_prefix="/api/purchase-items")


@purchase_items_bp.route("", methods=["GET"])
def get_purchase_items():
    """Return every purchase item in the database as JSON."""
    items = PurchaseItem.query.all()
    return jsonify([i.to_dict() for i in items]), 200


@purchase_items_bp.route("/<int:purchase_item_id>", methods=["GET"])
def get_purchase_item(purchase_item_id):
    """Return a single purchase item by its ID, or 404 if it doesn't exist."""
    item = PurchaseItem.query.get_or_404(purchase_item_id)
    return jsonify(item.to_dict()), 200


@purchase_items_bp.route("", methods=["POST"])
def create_purchase_item():
    """Create a new purchase item. Body: {purchase_id, variant_id, quantity, unit_cost, subtotal}"""
    data = request.get_json(silent=True) or {}
    purchase_id = data.get("purchase_id")
    variant_id = data.get("variant_id")
    quantity = data.get("quantity")
    unit_cost = data.get("unit_cost")
    subtotal = data.get("subtotal")

    if not all([purchase_id, variant_id, quantity, unit_cost is not None, subtotal is not None]):
        return jsonify({"error": "purchase_id, variant_id, quantity, unit_cost, and subtotal are all required"}), 400

    new_item = PurchaseItem(
        purchase_id=purchase_id,
        variant_id=variant_id,
        quantity=quantity,
        unit_cost=unit_cost,
        subtotal=subtotal,
    )
    db.session.add(new_item)
    db.session.commit()

    return jsonify(new_item.to_dict()), 201
