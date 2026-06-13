import uuid
from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class Role(db.Model):
    __tablename__ = "roles"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at  = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at  = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    users = db.relationship("UserRole", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id        = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username  = db.Column(db.String(30), unique=True, nullable=False)
    email     = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    profile = db.relationship("UserProfile", back_populates="user", uselist=False)
    roles   = db.relationship("UserRole", back_populates="user")
    trades = db.relationship("Trade", back_populates="user", lazy="dynamic")

    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.username}>"


class UserProfile(db.Model):
    __tablename__ = "users_profile"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    first_name = db.Column(db.String(100))
    last_name  = db.Column(db.String(100))
    time_zone  = db.Column(db.String(50), default="America/Bogota")

    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile {self.first_name} {self.last_name}>"

class UserRole(db.Model):
    __tablename__ = "users_roles"

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)

    user = db.relationship("User", back_populates="roles")
    role = db.relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"
