from app.extensions import db

class Autor(db.Model):
    __tablename__ = "autores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    pais = db.Column(db.String(50))
    libros = db.relationship("Libro", back_populates="autor", lazy=True)

    def to_dict(self):
        return  {"id":self.id,"nombre":self.nombre,  "pais":self.pais}