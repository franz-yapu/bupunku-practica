from sqlalchemy import exists, select

from app.extensions import db
from app.models import Autor, Libro


def obtener(autor_id):
    return db.session.get(Autor, autor_id)


def listar_paginado(pagina, por_pagina):
    consulta = select(Autor).order_by(Autor.id)
    return db.paginate(consulta, page=pagina, per_page=por_pagina, error_out=False)


def tiene_libros(autor_id):
    consulta = select(exists().where(Libro.autor_id == autor_id))
    return db.session.scalar(consulta)


def agregar(autor):
    db.session.add(autor)


def eliminar(autor):
    db.session.delete(autor)
