from app.extensions import db
from datetime import datetime, timezone

class Strategy(db.Model):
    __tablename__ = "strategies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    trades = db.relationship(
        "Trade",
        back_populates="strategy",
        lazy="dynamic",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Strategy {self.name}>"
