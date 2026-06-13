import uuid
import enum
from app.extensions import db
from datetime import datetime, timezone

class TradeDirection(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradePhase(enum.Enum):
    BEFORE = "BEFORE"
    DURING = "DURING"
    AFTER = "AFTER"

class Trade(db.Model):
    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey("strategies.id"), nullable=False)
    symbol_id = db.Column(db.Integer, db.ForeignKey("symbols.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    direction = db.Column(db.Enum(TradeDirection), nullable=False)  # "Buy" or "Sell"
    classification = db.Column(db.String(10), nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    stop_loss = db.Column(db.Float, nullable=True)
    take_profit = db.Column(db.Float, nullable=True)
    exit_price = db.Column(db.Float, nullable=True)
    lot_size = db.Column(db.Float, nullable=False)
    profit_loss = db.Column(db.Float, nullable=True)
    rr_ratio = db.Column(db.Float, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    trade_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # --- Relationships
    user = db.relationship("User", back_populates="trades")
    strategy = db.relationship("Strategy", back_populates="trades")
    symbol = db.relationship("Symbol", back_populates="trades")
    emotions = db.relationship("TradeEmotion", back_populates="trade", cascade="all, delete-orphan")
    tags = db.relationship("TradeTag", back_populates="trade", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trade {self.id} - User {self.user_id}>"

class TradeEmotion(db.Model):
    __tablename__ = "trade_emotions"

    trade_id = db.Column(
        db.Integer,
        db.ForeignKey("trades.id", ondelete="CASCADE"),
        primary_key=True
    )

    emotion_id = db.Column(
        db.Integer,
        db.ForeignKey("emotions.id", ondelete="CASCADE"),
        primary_key=True
    )
    phase = db.Column(db.Enum(TradePhase), nullable=False)
    note = db.Column(db.Text, nullable=True)

    trade = db.relationship("Trade", back_populates="emotions")
    emotion = db.relationship("Emotion", back_populates="trades")

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"

class TradeTag(db.Model):
    __tablename__ = "trade_tags"

    trade_id = db.Column(
        db.Integer,
        db.ForeignKey("trades.id", ondelete="CASCADE"),
        primary_key=True
    )

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )

    trade = db.relationship("Trade", back_populates="tags")
    tag = db.relationship("Tag", back_populates="trades")

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"
