from flask import Blueprint

from app.services import prestamos_service

from .validacion import entero, leer_json

bp = Blueprint("prestamos", __name__, url_prefix="/prestamos")


@bp.post("")
def prestar():
    datos = leer_json()
    prestamo = prestamos_service.prestar(
        libro_id=entero(datos, "libro_id"),
        socio_id=entero(datos, "socio_id"),
    )
    return prestamo.to_dict(), 201


@bp.post("/<int:prestamo_id>/devolver")
def devolver(prestamo_id):
    prestamo = prestamos_service.devolver(prestamo_id)
    return prestamo.to_dict()
