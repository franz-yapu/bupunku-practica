from sqlalchemy import  select
from app.services.excepciones import NoEncontradoError

from app.extensions import db
from app.models import Libro

def obterner(libro_id, bloqueo=False):
    libro = db.session.get(Libro, libro_id , with_for_update=bloqueo)
    if not libro:
        raise NoEncontradoError(f"Libro con id {libro_id} no encontrado")
    return libro

def listar(disponible=None):
    consulta = select(Libro).order_by(Libro.id)
    if disponible is not None:
        consulta = consulta.where(Libro.disponible == disponible)
    return db.session.execute(consulta).scalars().all()

def de_autor(autor_id):
    consulta = select(Libro).where(Libro.autor_id == autor_id).order_by(Libro.id)
    return db.session.execute(consulta).scalars().all()

def agregar(libro):
    db.session.add(libro)
    db.session.commit()
    return libro
