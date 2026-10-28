from datetime import datetime, timezone

from app.extensions import db


def ahora():
    return datetime.now(timezone.utc)


class Prestamo(db.Model):
    __tablename__ = "prestamos"

    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id"), nullable=False, index=True)
    socio_id = db.Column(db.Integer, db.ForeignKey("socios.id"), nullable=False, index=True)
    fecha_prestamo = db.Column(db.DateTime(timezone=True), nullable=False, default=ahora)
    fecha_devolucion = db.Column(db.DateTime(timezone=True))

    libro = db.relationship("Libro")
    socio = db.relationship("Socio")

    def to_dict(self):
        return {
            "id": self.id,
            "libro_id": self.libro_id,
            "socio_id": self.socio_id,
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion": self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
        }
