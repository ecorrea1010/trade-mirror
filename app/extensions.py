from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_migrate import Migrate

db            = SQLAlchemy()
login_manager = LoginManager()
migrate       = Migrate()

class FakeUser(UserMixin):
    id       = 1
    username = "admin"

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return User.query.get(user_id)
