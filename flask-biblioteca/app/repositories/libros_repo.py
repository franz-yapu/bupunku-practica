from sqlalchemy import select

from app.extensions import db
from app.models import Libro


def obtener(libro_id, bloquear=False):
    # bloquear=True -> SELECT ... FOR UPDATE en PostgreSQL
    return db.session.get(Libro, libro_id, with_for_update=bloquear)


def listar(disponible=None):
    consulta = select(Libro).order_by(Libro.id)
    if disponible is not None:
        consulta = consulta.where(Libro.disponible == disponible)
    return db.session.scalars(consulta).all()


def de_autor(autor_id):
    consulta = select(Libro).where(Libro.autor_id == autor_id).order_by(Libro.id)
    return db.session.scalars(consulta).all()


def agregar(libro):
    db.session.add(libro)
