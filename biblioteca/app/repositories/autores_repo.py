from sqlalchemy import exists, select


from app.extensions import db
from app.models import Autor, Libro
from app.services.excepciones import NoEncontradoError

def obtener(autor_id):
    autor = db.session.get(Autor, autor_id)
    if not autor:
        raise NoEncontradoError(f"Autor con id {autor_id} no encontrado")
    return autor

def listar_paginado(paginado, por_pagina):
    consulta = select(Autor).order_by(Autor.id)
    return db.paginate(consulta, page=paginado, per_page=por_pagina , errror_out=False)

def tiene_libros(autor_id):
    consulta = select(exists().where(Libro.autor_id == autor_id))
    return db.session.execute(consulta).scalar()

def agregar(autor):
    db.session.add(autor)
    db.session.commit()
    return autor

def eliminar(autor):
    db.session.delete(autor)
    db.session.commit()
    