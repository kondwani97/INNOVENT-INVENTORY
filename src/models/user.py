from datetime import datetime, timezone
from werkzeug.security import generate_password_hash,  check_password_hash

from src.extensions import db


class User(db.Model):
    __tablename__ = "app_user"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey("business.business_id"), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def set_password(self, plain_password):
        """Hash and store a plain-text password. Never store the plain version."""
        self.password_hash = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        """Verify a plain-text password against the stored hash."""
        return check_password_hash(self.password_hash, plain_password)

    def to_dict(self):
        """Convert this row into a plain dict, ready for jsonify(). Never includes password_hash."""
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role_id": self.role_id,
            "business_id": self.business_id,
            "is_active": self.is_active,
        }
        
        