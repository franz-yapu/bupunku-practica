from aqlalchemy import  select

from app.extensions import db
from app.models import Prestamo

def obtener(prestamo_id , bloqueo=False):
    prestamo = db.session.get(Prestamo, prestamo_id , with_for_update=bloqueo)
    return prestamo  

def activos_de_socio(socio_id):
    consulta = select(Prestamo).where(Prestamo.socio_id == socio_id , Prestamo.fecha_devolucion == None)
    return db.session.execute(consulta).scalars().all()

def agregar(prestamo):
    db.session.add(prestamo)
    db.session.commit()
    return prestamo