from datetime import datetime, timezone

from src.extensions import db


class ProductVariant(db.Model):
    __tablename__ = "product_variant"

    variant_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.product_id"), nullable=False)
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    buying_price = db.Column(db.Numeric(12, 2), nullable=False)
    selling_price = db.Column(db.Numeric(12, 2), nullable=False)
    quantity_on_hand = db.Column(db.Integer, nullable=False, default=0)
    reorder_level = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "variant_id": self.variant_id,
            "product_id": self.product_id,
            "color": self.color,
            "size": self.size,
            "buying_price": float(self.buying_price),
            "selling_price": float(self.selling_price),
            "quantity_on_hand": self.quantity_on_hand,
            "reorder_level": self.reorder_level,
        }