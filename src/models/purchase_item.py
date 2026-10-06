from src.extensions import db


class PurchaseItem(db.Model):
    __tablename__ = "purchase_item"

    purchase_item_id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey("purchase.purchase_id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variant.variant_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Numeric(12, 2), nullable=False)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False)

    def to_dict(self):
        return {
            "purchase_item_id": self.purchase_item_id,
            "purchase_id": self.purchase_id,
            "variant_id": self.variant_id,
            "quantity": self.quantity,
            "unit_cost": float(self.unit_cost),
            "subtotal": float(self.subtotal),
        }