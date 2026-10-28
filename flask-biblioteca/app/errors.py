from werkzeug.exceptions import HTTPException

from .extensions import db
from .services.excepciones import (
    Conflicto,
    DatosInvalidos,
    ErrorDeNegocio,
    NoEncontrado,
    ReglaDeNegocio,
)

# Traducción: error de negocio -> código HTTP. Solo esta capa conoce HTTP.
CODIGOS = {
    DatosInvalidos: 400,
    NoEncontrado: 404,
    Conflicto: 409,
    ReglaDeNegocio: 422,
}


def registrar_errores(app):
    @app.errorhandler(ErrorDeNegocio)
    def error_de_negocio(e):
        return {"error": e.mensaje}, CODIGOS.get(type(e), 400)

    @app.errorhandler(HTTPException)
    def error_http(e):
        return {"error": e.name}, e.code

    @app.errorhandler(Exception)
    def error_inesperado(e):
        db.session.rollback()
        app.logger.exception("Error no controlado")
        return {"error": "Error interno del servidor"}, 500
