from datetime import datetime, timezone

from src.extensions import db

class Product(db.Model):
    __tablename__ = "product"

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey("supplier.supplier_id"))
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(30), nullable=False, default="active")
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "supplier_id": self.supplier_id,
            "image_url": self.image_url,
            "status": self.status,
        }