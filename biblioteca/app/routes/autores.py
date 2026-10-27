from flask import Blueprint

from app.services import autores_service

from .validacion import leer_json, pagina_de_query, texto

bp = Blueprint("autores", __name__, url_prefix="/autores")


@bp.get("")
def listar():
    resultado = autores_service.listar(pagina_de_query())
    return {
        "items": [a.to_dict() for a in resultado.items],
        "pagina": resultado.page,
        "paginas": resultado.pages,
        "total": resultado.total,
    }


@bp.post("")
def crear():
    datos = leer_json()
    autor = autores_service.crear(
        nombre=texto(datos, "nombre", 120),
        pais=texto(datos, "pais", 80, obligatorio=False),
    )
    return autor.to_dict(), 201


@bp.get("/<int:autor_id>/libros")
def libros(autor_id):
    libros = autores_service.libros_de(autor_id)
    return {"items": [l.to_dict() for l in libros]}


@bp.delete("/<int:autor_id>")
def eliminar(autor_id):
    autores_service.eliminar(autor_id)
    return "", 204
