from werkzeug.exceptions import HTTPException

from .extensions import db
from .services.excepciones import (ErrorDeNegocion, DataInvalidaError, DataInvalidos, NoEncontradoError, conflictoError, ReglaDeNegocioError)



CODIGO_ERROR = {
    DataInvalidaError: 400,
    DataInvalidos: 400,
    NoEncontradoError: 404,
    conflictoError: 409,
    ReglaDeNegocioError: 422,
}

def registrar_errores(app):
    @app.errorhandler(ErrorDeNegocion)
    def error_de_negocio(e):
       return { "error": e.mensaje }, CODIGO_ERROR.get(type(e), 400)   

    @app.errorhandler(HTTPException)
    def error_http(e):
        return {
            "error": e.name,
        }, e.code

    @app.errorhandler(Exception)
    def error_inesperado(e):
        db.session.rollback()
        app.logger.exception("Error inesperado: %s", str(e))
        return {
            "error": "Error inesperado",
            "mensaje": str(e),
        }, 500