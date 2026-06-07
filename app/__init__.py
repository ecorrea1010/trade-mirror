import os
from flask import Flask
from app.extensions import db, login_manager, migrate

def create_app(config_name=None):
    app = Flask(__name__)

    # Toma el entorno de la variable de entorno, o usa development por defecto
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    from config import config
    app.config.from_object(config[config_name])

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Necesitas iniciar sesión."
    login_manager.login_message_category = "warning"

    # Carga el modelo de usuario
    with app.app_context():
        from app.models.user import Role, User, UserProfile, UserRole
        db.create_all()  # Crea las tablas si no existen

    # Registra blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.trades import trades
    app.register_blueprint(trades, url_prefix="/trades")

    # trades lo agregas cuando tengas las rutas listas
    # from app.routes.trades import trades
    # app.register_blueprint(trades, url_prefix="/trades")

    return app
