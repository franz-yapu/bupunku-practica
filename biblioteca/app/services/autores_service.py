from app.models import Autor
from app.repositories import autores_repo, libros_repo

from .excepciones import ConflictoError, NoEncontradoError
from .transaccion import transaccion

def listar(pagina=1, por_pagina=10):
    """Lista los autores con paginación."""
    return autores_repo.listar_paginado(pagina, por_pagina)

def crear(nombre, pais=None, ):
    """Crea un nuevo autor."""
    autor = Autor(nombre=nombre, pais=pais)
    with transaccion():
        autores_repo.agregar(autor)
    return autor


def libros_de(autor_id):
    """Obtiene los libros de un autor específico."""
    if  autores_repo.obtener(autor_id) is None:
     raise NoEncontradoError(f"Autor con id {autor_id} no encontrado")
    return libros_repo.de_autor(autor_id)

def eliminar(autor_id):
    """Elimina un autor si no tiene libros asociados."""
    autor = autores_repo.obtener(autor_id)
    if  autor is None:
        raise NoEncontradoError(f"Autor con id {autor_id} no encontrado")

    if autores_repo.tiene_libros(autor_id):
        raise ConflictoError(f"El autor con id {autor_id} tiene libros asociados y no puede ser eliminado.")

    with transaccion():
        autores_repo.eliminar(autor)