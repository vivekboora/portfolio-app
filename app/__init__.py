import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Make sure tables exist (safe no-op if they already do).
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app
