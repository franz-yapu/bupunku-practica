from app.extensions import db
from app.models import Prestamo
from app.repositories import prestamos_repo
 
 
def test_prestar_es_todo_o_nada(client, libro_id, socio_id, monkeypatch):
    agregar_real = prestamos_repo.agregar
 
    def agregar_y_fallar(prestamo):
        agregar_real(prestamo)
        raise RuntimeError("se cayó justo después de guardar el préstamo")
 
    monkeypatch.setattr(prestamos_repo, "agregar", agregar_y_fallar)
    r = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id})
 
    assert r.status_code == 500
    assert db.session.query(Prestamo).count() == 0 