from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException   # NUEVO

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///biblioteca.db"

    if config:
        app.config.update(config)

    db.init_app(app)

    from . import models
    from .routes import bp

    app.register_blueprint(bp)

    # NUEVO: cualquier error HTTP (404, 405, 400...) sale en JSON
    @app.errorhandler(HTTPException)
    def error_http(e):
        return {"error": e.name, "detalle": e.description}, e.code

    # NUEVO: errores inesperados (bugs) salen como 500 en JSON
    @app.errorhandler(500)
    def error_interno(e):
        return {"error": "Error interno del servidor"}, 500

    with app.app_context():
        db.create_all()

    return app