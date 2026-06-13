from app.extensions import db
from datetime import datetime, timezone

class Symbol(db.Model):
    __tablename__ = "symbols"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    trades = db.relationship("Trade", back_populates="symbol", lazy="dynamic")

    def __repr__(self):
        return f"<Symbol {self.name}>"
