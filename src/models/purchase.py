from datetime import datetime, timezone

from src.extensions import db


class Purchase(db.Model):
    __tablename__ = "purchase"

    purchase_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.supplier_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("app_user.user_id"), nullable=False)
    status = db.Column(db.String(30), nullable=False, default="pending")
    purchase_date = db.Column(db.Date, nullable=False)
    discount_type = db.Column(db.String(20))
    discount_value = db.Column(db.Numeric(12, 2))
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "purchase_id": self.purchase_id,
            "supplier_id": self.supplier_id,
            "user_id": self.user_id,
            "status": self.status,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "discount_type": self.discount_type,
            "discount_value": float(self.discount_value) if self.discount_value is not None else None,
            "total_amount": float(self.total_amount),
        }