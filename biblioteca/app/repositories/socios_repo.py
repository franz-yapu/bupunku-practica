from sqlalchemy import select
from app.extensions import db
from app.models import Socio


def obtener(socio_id):
    socio = db.session.get(Socio, socio_id)
    return socio

def por_email(socio_email):
    consulta = select(Socio).where(Socio.email == socio_email)
    return db.session.execute(consulta).scalars().first()

def aregar(socio):
    db.session.add(socio)
    db.session.commit()
    return socio