
from app.models import Prestamo
from app.models.prestamo import ahora
from app.repositories import libros_repo, prestamos_repo, socios_repo

from .excepciones import Conflicto, NoEncontrado
from .transaccion import transaccion


def prestar(libro_id, socio_id):
    with transaccion():
        if socios_repo.obtener(socio_id) is None:
            raise NoEncontrado("Socio no encontrado")

        libro = libros_repo.obtener(libro_id, bloquear=True)
        if libro is None:
            raise NoEncontrado("Libro no encontrado")
        if not libro.disponible:
            raise Conflicto("El libro ya está prestado")

        prestamo = Prestamo(libro_id=libro_id, socio_id=socio_id)
        prestamos_repo.agregar(prestamo)
        libro.disponible = False  # segundo cambio, en la MISMA transacción
    return prestamo


def devolver(prestamo_id):
    with transaccion():
        prestamo = prestamos_repo.obtener(prestamo_id, bloquear=True)
        if prestamo is None:
            raise NoEncontrado("Préstamo no encontrado")
        if prestamo.fecha_devolucion is not None:
            raise Conflicto("El préstamo ya fue devuelto")

        prestamo.fecha_devolucion = ahora()
        prestamo.libro.disponible = True
    return prestamo