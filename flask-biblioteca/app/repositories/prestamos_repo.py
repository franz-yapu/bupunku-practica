from sqlalchemy import select

from app.extensions import db
from app.models import Prestamo


def obtener(prestamo_id, bloquear=False):
    return db.session.get(Prestamo, prestamo_id, with_for_update=bloquear)


def activos_de_socio(socio_id):
    consulta = (
        select(Prestamo)
        .where(Prestamo.socio_id == socio_id, Prestamo.fecha_devolucion.is_(None))
        .order_by(Prestamo.id)
    )
    return db.session.scalars(consulta).all()


def agregar(prestamo):
    db.session.add(prestamo)
