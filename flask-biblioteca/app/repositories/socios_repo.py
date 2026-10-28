from sqlalchemy import select

from app.extensions import db
from app.models import Socio


def obtener(socio_id):
    return db.session.get(Socio, socio_id)


def por_email(email):
    return db.session.scalar(select(Socio).where(Socio.email == email))


def agregar(socio):
    db.session.add(socio)
