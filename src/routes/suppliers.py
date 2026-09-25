from flask import Blueprint, jsonify, request

from src.extensions import db
from src.models.supplier import Supplier

suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/api/suppliers")


@suppliers_bp.route("", methods=["GET"])
def get_suppliers():
    """Return every supplier in the database as JSON."""
    suppliers = Supplier.query.all()
    return jsonify([s.to_dict() for s in suppliers]), 200


@suppliers_bp.route("/<int:supplier_id>", methods=["GET"])
def get_supplier(supplier_id):
    """Return a single supplier by its ID, or 404 if it doesn't exist."""
    supplier = Supplier.query.get_or_404(supplier_id)
    return jsonify(supplier.to_dict()), 200


@suppliers_bp.route("", methods=["POST"])
def create_supplier():
    """Create a new supplier. Body: {name, contact_person, phone, email, address}"""
    data = request.get_json(silent=True) or {}
    name = data.get("name")

    if not name:
        return jsonify({"error": "name is required"}), 400

    new_supplier = Supplier(
        name=name,
        contact_person=data.get("contact_person"),
        phone=data.get("phone"),
        email=data.get("email"),
        address=data.get("address"),
    )
    db.session.add(new_supplier)
    db.session.commit()

    return jsonify(new_supplier.to_dict()), 201