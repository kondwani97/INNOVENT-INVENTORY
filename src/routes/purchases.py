from datetime import date

from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.purchase import Purchase

purchases_bp = Blueprint("purchases", __name__, url_prefix="/api/purchases")


@purchases_bp.route("", methods=["GET"])
def get_purchases():
    """Return every purchase in the database as JSON."""
    purchases = Purchase.query.all()
    return jsonify([p.to_dict() for p in purchases]), 200


@purchases_bp.route("/<int:purchase_id>", methods=["GET"])
def get_purchase(purchase_id):
    """Return a single purchase by its ID, or 404 if it doesn't exist."""
    purchase = Purchase.query.get_or_404(purchase_id)
    return jsonify(purchase.to_dict()), 200


@purchases_bp.route("", methods=["POST"])
def create_purchase():
    """Create a new purchase. Body: {supplier_id, user_id, purchase_date, total_amount, status, discount_type, discount_value}"""
    data = request.get_json(silent=True) or {}
    supplier_id = data.get("supplier_id")
    user_id = data.get("user_id")
    total_amount = data.get("total_amount")

    if not supplier_id or not user_id or total_amount is None:
        return jsonify({"error": "supplier_id, user_id, and total_amount are required"}), 400

    purchase_date_str = data.get("purchase_date")
    purchase_date = date.fromisoformat(purchase_date_str) if purchase_date_str else date.today()

    new_purchase = Purchase(
        supplier_id=supplier_id,
        user_id=user_id,
        status=data.get("status", "pending"),
        purchase_date=purchase_date,
        discount_type=data.get("discount_type"),
        discount_value=data.get("discount_value"),
        total_amount=total_amount,
    )
    db.session.add(new_purchase)
    db.session.commit()

    return jsonify(new_purchase.to_dict()), 201