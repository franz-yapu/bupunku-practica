from app.models import Autor
from app.repositories import autores_repo, libros_repo

from .excepciones import Conflicto, NoEncontrado
from .transaccion import transaccion


def listar(pagina, por_pagina=10):
    return autores_repo.listar_paginado(pagina, por_pagina)


def crear(nombre, pais=None):
    autor = Autor(nombre=nombre, pais=pais)
    with transaccion():
        autores_repo.agregar(autor)
    return autor


def libros_de(autor_id):
    if autores_repo.obtener(autor_id) is None:
        raise NoEncontrado("Autor no encontrado")
    return libros_repo.de_autor(autor_id)


def eliminar(autor_id):
    autor = autores_repo.obtener(autor_id)
    if autor is None:
        raise NoEncontrado("Autor no encontrado")
    if autores_repo.tiene_libros(autor_id):
        raise Conflicto("El autor tiene libros; no se puede borrar")
    with transaccion():
        autores_repo.eliminar(autor)
