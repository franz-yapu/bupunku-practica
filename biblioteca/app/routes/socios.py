from flask import Blueprint

from app.services import socios_service
from app.services.excepciones import DatosInvalidos

from .validacion import leer_json, texto

bp = Blueprint("socios", __name__, url_prefix="/socios")


@bp.post("")
def crear():
    datos = leer_json()
    email = texto(datos, "email", 160)
    if "@" not in email:
        raise DatosInvalidos("'email' no es válido")
    socio = socios_service.crear(nombre=texto(datos, "nombre", 120), email=email)
    return socio.to_dict(), 201


@bp.get("/<int:socio_id>/prestamos")
def prestamos(socio_id):
    activos = socios_service.prestamos_activos(socio_id)
    return {"items": [p.to_dict() for p in activos]}