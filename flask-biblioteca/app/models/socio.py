from app.extensions import db


class Socio(db.Model):
    __tablename__ = "socios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "email": self.email}
