from datetime import date

from app.models import Libro
from app.repositories import autores_repo, libros_repo

from .excepciones import NoEncontradoError, ReglaDeNegocioError
from .transaccion import transaccion


def _validar_anio(anio):
    if anio is not None and anio > date.today().year:
        raise ReglaDeNegocioError("El año no puede ser futuro")


def _validar_autor(autor_id):
    if autores_repo.obtener(autor_id) is None:
        raise NoEncontradoError("Autor no encontrado")


def listar(disponible=None):
    return libros_repo.listar(disponible)


def crear(titulo, autor_id, anio=None, disponible=True):
    _validar_autor(autor_id)
    _validar_anio(anio)
    libro = Libro(titulo=titulo, autor_id=autor_id, anio=anio, disponible=disponible)
    with transaccion():
        libros_repo.agregar(libro)
    return libro


def actualizar(libro_id, cambios):
    libro = libros_repo.obtener(libro_id)
    if libro is None:
        raise NoEncontradoError("Libro no encontrado")
    if "autor_id" in cambios:
        _validar_autor(cambios["autor_id"])
    if "anio" in cambios:
        _validar_anio(cambios["anio"])

    with transaccion():
        for campo, valor in cambios.items():
            setattr(libro, campo, valor)
    return libro