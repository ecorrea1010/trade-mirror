from app.extensions import db
from datetime import datetime, timezone

class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    trades = db.relationship("TradeTag", back_populates="tag", lazy="dynamic")

    def __repr__(self):
        return f"<Tag {self.name}>"
