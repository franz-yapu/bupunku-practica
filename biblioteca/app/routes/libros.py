from flask import Blueprint, request

from app.services import libros_service
from app.services.excepciones import DatosInvalidos

from .validacion import booleano, entero, leer_json, texto

bp = Blueprint("libros", __name__, url_prefix="/libros")


@bp.get("")
def listar():
    filtro = request.args.get("disponible")
    disponible = None
    if filtro is not None:
        if filtro.lower() not in ("true", "false"):
            raise DatosInvalidos("'disponible' debe ser true o false")
        disponible = filtro.lower() == "true"
    return {"items": [l.to_dict() for l in libros_service.listar(disponible)]}


@bp.post("")
def crear():
    datos = leer_json()
    libro = libros_service.crear(
        titulo=texto(datos, "titulo", 200),
        autor_id=entero(datos, "autor_id"),
        anio=entero(datos, "anio", obligatorio=False),
        disponible=booleano(datos, "disponible", por_defecto=True),
    )
    return libro.to_dict(), 201


@bp.patch("/<int:libro_id>")
def actualizar(libro_id):
    datos = leer_json()
    cambios = {}
    if "titulo" in datos:
        cambios["titulo"] = texto(datos, "titulo", 200)
    if "anio" in datos:
        cambios["anio"] = entero(datos, "anio", obligatorio=False)
    if "disponible" in datos:
        cambios["disponible"] = booleano(datos, "disponible", por_defecto=True)
    if "autor_id" in datos:
        cambios["autor_id"] = entero(datos, "autor_id")

    libro = libros_service.actualizar(libro_id, cambios)
    return libro.to_dict()