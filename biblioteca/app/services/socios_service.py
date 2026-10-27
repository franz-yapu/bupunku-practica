from sqlalchemy.exc import IntegrityError

from app.models import Socio
from app.repositories import prestamos_repo, socios_repo

from .excepciones import ConflictoError, NoEncontradoError
from .transaccion import transaccion


def crear(nombre, email):
    email = email.lower()
    if socios_repo.por_email(email) is not None:
        raise ConflictoError("Ya existe un socio con ese email")

    socio = Socio(nombre=nombre, email=email)
    try:
        with transaccion():
            socios_repo.agregar(socio)
    except IntegrityError:
        # Dos peticiones al mismo tiempo pasaron el chequeo de arriba:
        # la restricción UNIQUE de la base de datos es la última defensa.
        raise ConflictoError("Ya existe un socio con ese email")
    return socio


def prestamos_activos(socio_id):
    if socios_repo.obtener(socio_id) is None:
        raise NoEncontradoError("Socio no encontrado")
    return prestamos_repo.activos_de_socio(socio_id)