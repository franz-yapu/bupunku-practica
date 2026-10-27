from app.extensions import db

class Libro(db.Model):
    __tablename__ = "libros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    anio = db.Column(db.Integer)
    disponible = db.Column(db.Boolean, nullable=False, default=True)
   

    autor_id = db.Column(db.Integer, db.ForeignKey("autores.id"), nullable=False, index=True)

    autor = db.relationship("Autor", back_populates="libros", lazy=True)
    def __repr__(self):
        return {
            "id": self.id,
            "titulo": self.titulo, 
            "autor": self.autor.nombre if self.autor else None,
            "anio": self.anio,
            "disponible": self.disponible
            }