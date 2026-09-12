from src.extensions import db


class Role(db.Model):
    __tablename__ = "role"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Convert this row into a plain dict, ready for jsonify()."""
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
        }
