from app.extensions import db
from datetime import datetime, timezone

class Emotion(db.Model):
    __tablename__ = "emotions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category_emotions.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    trades = db.relationship("TradeEmotion", back_populates="emotion", lazy="dynamic")
    category = db.relationship(
        "CategoryEmotion",
        back_populates="emotions"
    )

    def __repr__(self):
        return f"<Emotion {self.name}>"
