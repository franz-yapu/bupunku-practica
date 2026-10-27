from datetime import datetime , timezone

from app.extensions import db   

def  ahoa():
    return datetime.now(timezone.utc)   

class Prestamo(db.Model):
    __tablename__ = "prestamos"
    id = db.Column(db.Integer, primary_key=True)
    
    libro_id = db.Column(db.Integer, db.ForeignKey("libros.id"), nullable=False, index=True)
    socio_id = db.Column(db.Integer, db.ForeignKey("socios.id"), nullable=False, index=True)
    fecha_prestamo = db.Column(db.DateTime(timezone.utc), nullable=False, default=ahoa)
    fecha_devolucion = db.Column(db.DateTime(timezone.utc))

    libro = db.relationship("Libro", backref=db.backref("prestamos", lazy=True))
    socio = db.relationship("Socio", backref=db.backref("prestamos", lazy=True))

    def __repr__(self):
        return {
            "id": self.id,
            "libro": self.libro.titulo if self.libro else None,
            "socio": self.socio.nombre if self.socio else None,
            "fecha_prestamo": self.fecha_prestamo.isoformat(),
            "fecha_devolucion": self.fecha_devolucion.isoformat() if self.fecha_devolucion else None,
        }