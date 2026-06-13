from app.extensions import db
from datetime import datetime, timezone

class CategoryEmotion(db.Model):
    __tablename__ = "category_emotions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    emotions = db.relationship(
        "Emotion",
        back_populates="category",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"<Emotion {self.name}>"
