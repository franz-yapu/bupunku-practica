from datetime import date 
from flask import Blueprint, request

from . import db
from .models import Autor, Libro

bp = Blueprint("api", __name__)


@bp.get("/autores")
def listar_autores():
    pagina = request.args.get("pagina", 1, type=int)
    consulta = db.select(Autor).order_by(Autor.id)
    resultado = db.paginate(consulta, page=pagina, per_page=10, error_out=False)

    return {
        "items": [a.to_dict() for a in resultado.items],
        "pagina": resultado.page,
        "total": resultado.total,
        "paginas": resultado.pages,
    }


@bp.post("/autores")
def crear_autor():
    datos = request.get_json(silent=True) or {}
    nombre = datos.get("nombre")

    if not isinstance(nombre, str) or not nombre.strip():
        return {"error": "El campo 'nombre' es obligatorio"}, 400

    autor = Autor(nombre=nombre.strip(), pais=datos.get("pais"))
    db.session.add(autor)
    db.session.commit()
    return autor.to_dict(), 201


@bp.get("/autores/<int:autor_id>/libros")
def libros_de_autor(autor_id):
    autor = db.session.get(Autor, autor_id)
    if autor is None:
        return {"error": "Autor no encontrado"}, 404

    return {"items": [l.to_dict() for l in autor.libros]}


@bp.delete("/autores/<int:autor_id>")
def borrar_autor(autor_id):
    autor = db.session.get(Autor, autor_id)
    if autor is None:
        return {"error": "Autor no encontrado"}, 404

    if autor.libros:
        return {"error": "El autor tiene libros; no se puede borrar"}, 409

    db.session.delete(autor)
    db.session.commit()
    return "", 204


#####   libros #### 
def _es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


@bp.get("/libros")
def listar_libros():
    consulta = db.select(Libro).order_by(Libro.id)

    filtro = request.args.get("disponible")
    if filtro is not None:
        filtro = filtro.lower()
        if filtro not in ("true", "false"):
            return {"error": "'disponible' debe ser true o false"}, 400
        consulta = consulta.where(Libro.disponible == (filtro == "true"))

    libros = db.session.scalars(consulta).all()
    return {"items": [l.to_dict() for l in libros]}


@bp.post("/libros")
def crear_libro():
    datos = request.get_json(silent=True) or {}
    titulo = datos.get("titulo")
    autor_id = datos.get("autor_id")
    anio = datos.get("anio")
    disponible = datos.get("disponible", True)

    # 400: falta un dato o el tipo está mal
    if not isinstance(titulo, str) or not titulo.strip():
        return {"error": "El campo 'titulo' es obligatorio"}, 400
    if not _es_entero(autor_id):
        return {"error": "El campo 'autor_id' es obligatorio y debe ser entero"}, 400
    if anio is not None and not _es_entero(anio):
        return {"error": "El campo 'anio' debe ser entero"}, 400
    if not isinstance(disponible, bool):
        return {"error": "El campo 'disponible' debe ser true o false"}, 400

    # 404: el autor no existe
    if db.session.get(Autor, autor_id) is None:
        return {"error": "Autor no encontrado"}, 404

    # 422: regla de negocio
    if anio is not None and anio > date.today().year:
        return {"error": "El año no puede ser futuro"}, 422

    libro = Libro(
        titulo=titulo.strip(),
        anio=anio,
        disponible=disponible,
        autor_id=autor_id,
    )
    db.session.add(libro)
    db.session.commit()
    return libro.to_dict(), 201


@bp.patch("/libros/<int:libro_id>")
def actualizar_libro(libro_id):
    libro = db.session.get(Libro, libro_id)
    if libro is None:
        return {"error": "Libro no encontrado"}, 404

    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return {"error": "Se esperaba un JSON"}, 400

    cambios = {}

    if "titulo" in datos:
        titulo = datos["titulo"]
        if not isinstance(titulo, str) or not titulo.strip():
            return {"error": "'titulo' no puede estar vacío"}, 400
        cambios["titulo"] = titulo.strip()

    if "anio" in datos:
        anio = datos["anio"]
        if anio is not None and not _es_entero(anio):
            return {"error": "'anio' debe ser entero"}, 400
        if anio is not None and anio > date.today().year:
            return {"error": "El año no puede ser futuro"}, 422
        cambios["anio"] = anio

    if "disponible" in datos:
        if not isinstance(datos["disponible"], bool):
            return {"error": "'disponible' debe ser true o false"}, 400
        cambios["disponible"] = datos["disponible"]

    if "autor_id" in datos:
        autor_id = datos["autor_id"]
        if not _es_entero(autor_id):
            return {"error": "'autor_id' debe ser entero"}, 400
        if db.session.get(Autor, autor_id) is None:
            return {"error": "Autor no encontrado"}, 404
        cambios["autor_id"] = autor_id

    # Recién aquí se aplica todo, porque ya pasó todas las validaciones
    for campo, valor in cambios.items():
        setattr(libro, campo, valor)

    db.session.commit()
    return libro.to_dict()