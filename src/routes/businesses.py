from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.business import Business

businesses_bp = Blueprint("businesses", __name__, url_prefix="/api/businesses")

@businesses_bp.route("", methods=["GET"])
def get_businesses():
    """Return every business in the database as JSON."""
    businesses = Business.query.all()
    return jsonify([b.to_dict() for b in businesses]), 200

@businesses_bp.route("/<int:business_id>", methods=["GET"])
def get_business(business_id):
    """Return a single business by its ID, or 404 if it doesn't exist."""
    business = Business.query.get_or_404(business_id)
    return jsonify(business.to_dict()), 200

@businesses_bp.route("", methods=["POST"])
def create_business():
    """Create a new business from JSON body: {"business_name": "Kondwani's Shop"}"""
    data = request.get_json(silent=True) or {}
    business_name = data.get("business_name")

    if not business_name:
        return jsonify({"error": "business_name is required"}), 400

    new_business = Business(business_name=business_name)
    db.session.add(new_business)
    db.session.commit()

    return jsonify(new_business.to_dict()), 201