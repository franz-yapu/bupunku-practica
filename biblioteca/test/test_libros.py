from datetime import date


def test_crear_libro_disponible_por_defecto(client, autor_id):
    r = client.post("/libros", json={"titulo": "Ficciones", "autor_id": autor_id})
    assert r.status_code == 201
    assert r.get_json()["disponible"] is True


def test_autor_inexistente_da_404(client):
    r = client.post("/libros", json={"titulo": "X", "autor_id": 999})
    assert r.status_code == 404


def test_anio_futuro_da_422(client, autor_id):
    r = client.post("/libros", json={"titulo": "X", "autor_id": autor_id, "anio": date.today().year + 1})
    assert r.status_code == 422


def test_patch_cambia_solo_lo_enviado(client, libro_id):
    r = client.patch(f"/libros/{libro_id}", json={"disponible": False})
    assert r.status_code == 200
    assert r.get_json()["disponible"] is False
    assert r.get_json()["titulo"] == "Ficciones"