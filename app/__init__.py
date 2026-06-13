import os
import click  # 👈 agregar esta línea
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
        from app.models.trades.category_emotion import CategoryEmotion
        from app.models.trades.emotion import Emotion
        from app.models.trades.strategy import Strategy
        from app.models.trades.symbol import Symbol
        from app.models.trades.tag import Tag
        from app.models.trades.trade import Trade, TradeEmotion, TradeTag
        db.create_all()  # Crea las tablas si no existen

    # Registra blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    from app.routes.trades import trades
    app.register_blueprint(trades, url_prefix="/trades")

    # trades lo agregas cuando tengas las rutas listas
    # from app.routes.trades import trades
    # app.register_blueprint(trades, url_prefix="/trades")

    # ---------------------------------------------------------------------------
    # Datos
    # ---------------------------------------------------------------------------

    CATEGORY_EMOTIONS = [
        {
            "name": "Positivas",
            "description": "Emociones que favorecen la ejecución disciplinada",
        },
        {
            "name": "Negativas",
            "description": "Emociones que suelen afectar la toma de decisiones",
        },
        {
            "name": "Neutras",
            "description": "Estados emocionales sin carga positiva o negativa marcada",
        },
        {
            "name": "Impulsividad",
            "description": "Emociones asociadas a decisiones apresuradas",
        },
        {
            "name": "Aversión al riesgo",
            "description": "Emociones relacionadas con miedo o inseguridad",
        },
        {
            "name": "Exceso de confianza",
            "description": "Emociones asociadas a sobreestimación de habilidades",
        },
        {
            "name": "Fatiga mental",
            "description": "Estados emocionales derivados del cansancio",
        },
    ]

    EMOTIONS = [
        # Positivas
        {"name": "Confianza",     "category": "Positivas"},
        {"name": "Disciplina",    "category": "Positivas"},
        {"name": "Paciencia",     "category": "Positivas"},
        {"name": "Calma",         "category": "Positivas"},
        {"name": "Claridad",      "category": "Positivas"},
        {"name": "Concentración", "category": "Positivas"},
        {"name": "Determinación", "category": "Positivas"},
        {"name": "Satisfacción",  "category": "Positivas"},
        # Negativas
        {"name": "Frustración",   "category": "Negativas"},
        {"name": "Ira",           "category": "Negativas"},
        {"name": "Estrés",        "category": "Negativas"},
        {"name": "Desmotivación", "category": "Negativas"},
        {"name": "Arrepentimiento", "category": "Negativas"},
        {"name": "Culpa",         "category": "Negativas"},
        {"name": "Tristeza",      "category": "Negativas"},
        # Neutras
        {"name": "Expectativa",   "category": "Neutras"},
        {"name": "Curiosidad",    "category": "Neutras"},
        {"name": "Observación",   "category": "Neutras"},
        {"name": "Prudencia",     "category": "Neutras"},
        # Impulsividad
        {"name": "FOMO",          "category": "Impulsividad"},
        {"name": "Impaciencia",   "category": "Impulsividad"},
        {"name": "Excitación excesiva", "category": "Impulsividad"},
        {"name": "Euforia",       "category": "Impulsividad"},
        {"name": "Venganza",      "category": "Impulsividad"},
        # Aversión al riesgo
        {"name": "Miedo",      "category": "Aversión al riesgo"},
        {"name": "Ansiedad",   "category": "Aversión al riesgo"},
        {"name": "Inseguridad", "category": "Aversión al riesgo"},
        {"name": "Duda",        "category": "Aversión al riesgo"},
        {"name": "Nerviosismo", "category": "Aversión al riesgo"},
        {"name": "Pánico",      "category": "Aversión al riesgo"},
        # Exceso de confianza
        {"name": "Sobreconfianza", "category": "Exceso de confianza"},
        {"name": "Codicia",      "category": "Exceso de confianza"},
        {"name": "Invulnerabilidad", "category": "Exceso de confianza"},
        {"name": "Arrogancia",     "category": "Exceso de confianza"},
        # Fatiga mental
        {"name": "Cansancio",      "category": "Fatiga mental"},
        {"name": "Agotamiento",    "category": "Fatiga mental"},
        {"name": "Saturación",     "category": "Fatiga mental"},
        {"name": "Falta de concentración", "category": "Fatiga mental"},
    ]

    SYMBOLS = [
        # Forex majors
        {"name": "EUR/USD", "category": "Forex",       "description": "Euro / Dólar estadounidense"},
        {"name": "GBP/USD", "category": "Forex",       "description": "Libra esterlina / Dólar"},
        {"name": "USD/JPY", "category": "Forex",       "description": "Dólar / Yen japonés"},
        {"name": "USD/CHF", "category": "Forex",       "description": "Dólar / Franco suizo"},
        {"name": "AUD/USD", "category": "Forex",       "description": "Dólar australiano / Dólar"},
        {"name": "USD/CAD", "category": "Forex",       "description": "Dólar / Dólar canadiense"},
        {"name": "NZD/USD", "category": "Forex",       "description": "Dólar neozelandés / Dólar"},
        {"name": "AUD/CHF", "category": "Forex",       "description": "Dólar australiano / Franco suizo"},
        # Forex minors
        {"name": "EUR/GBP", "category": "Forex",       "description": "Euro / Libra esterlina"},
        {"name": "EUR/JPY", "category": "Forex",       "description": "Euro / Yen japonés"},
        {"name": "GBP/JPY", "category": "Forex",       "description": "Libra / Yen japonés"},
        # Índices
        {"name": "US30",    "category": "Índices",     "description": "Dow Jones Industrial Average"},
        {"name": "US500",   "category": "Índices",     "description": "S&P 500"},
        {"name": "US100",   "category": "Índices",     "description": "Nasdaq 100"},
        {"name": "GER40",   "category": "Índices",     "description": "DAX 40"},
        # Crypto
        {"name": "BTC/USD", "category": "Crypto",      "description": "Bitcoin / Dólar"},
        {"name": "ETH/USD", "category": "Crypto",      "description": "Ethereum / Dólar"},
        {"name": "XRP/USD", "category": "Crypto",      "description": "Ripple / Dólar"},
        # Commodities
        {"name": "XAUUSD",  "category": "Commodities", "description": "Oro / Dólar"},
        {"name": "XAGUSD",  "category": "Commodities", "description": "Plata / Dólar"},
        {"name": "USOIL",   "category": "Commodities", "description": "Petróleo crudo WTI"},
    ]

    # ---------------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------------
    
    def _seed_categories():
        from app.models.trades.category_emotion import CategoryEmotion
        count = 0
        for data in CATEGORY_EMOTIONS:
            exists = CategoryEmotion.query.filter_by(name=data["name"]).first()
            if not exists:
                db.session.add(CategoryEmotion(**data))
                count += 1
        db.session.commit()
        click.echo(f"  ✔ category_emotions: {count} insertadas")
    
    
    def _seed_emotions():
        from app.models.trades.emotion import Emotion
        count = 0
        for data in EMOTIONS:
            exists = Emotion.query.filter_by(name=data["name"]).first()
            if not exists:
                category = CategoryEmotion.query.filter_by(name=data["category"]).first()
                if not category:
                    click.echo(f"  ⚠ Categoría '{data['category']}' no encontrada — omitiendo '{data['name']}'")
                    continue
                db.session.add(Emotion(name=data["name"], category_id=category.id))
                count += 1
        db.session.commit()
        click.echo(f"  ✔ emotions: {count} insertadas")
    
    def _seed_symbols():
        from app.models.trades.symbol import Symbol
        count = 0
        for data in SYMBOLS:
            exists = Symbol.query.filter_by(name=data["name"]).first()
            if not exists:
                db.session.add(Symbol(**data))
                count += 1
        db.session.commit()
        click.echo(f"  ✔ symbols: {count} insertadas")

    # Comando seed para poblar roles iniciales
    @app.cli.command("seed")
    @click.pass_context
    def seed_run(ctx):
        """Pobla las tablas de dimensiones con datos iniciales."""
        with app.app_context():
            click.echo("Iniciando seed...")
            _seed_categories()
            _seed_emotions()
            _seed_symbols()
            click.echo("Seed completado ✔")

    return app
