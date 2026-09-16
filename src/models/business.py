from src.extensions import db

class Business(db.Model):
    __tablename__ = "business"
    
    business_id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(150), nullable=False)
    
    def to_dict(self):
        """Convert this row into a plain dict, ready for jsonify()."""
        return {
            "business_id": self.business_id,
            "business_name": self.business_name,
        } 