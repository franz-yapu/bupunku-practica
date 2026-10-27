from . import db


class Autor(db.Model):
    __tablename__ = "autores"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    pais = db.Column(db.String(80), nullable=True)

    libros = db.relationship("Libro", back_populates="autor")

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "pais": self.pais}


class Libro(db.Model):
    __tablename__ = "libros"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    anio = db.Column(db.Integer, nullable=True)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
    autor_id = db.Column(db.Integer, db.ForeignKey("autores.id"), nullable=False)

    autor = db.relationship("Autor", back_populates="libros")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "anio": self.anio,
            "disponible": self.disponible,
            "autor_id": self.autor_id,
        }