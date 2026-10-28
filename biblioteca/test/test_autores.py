def test_crear_autor_sin_nombre_da_400(client):
    r = client.post("/autores", json={"pais": "Chile"})
    assert r.status_code == 400


def test_nombre_demasiado_largo_da_400(client):
    r = client.post("/autores", json={"nombre": "a" * 121})
    assert r.status_code == 400


def test_pagina_negativa_da_400(client):
    assert client.get("/autores?pagina=-1").status_code == 400


def test_no_borra_autor_con_libros(client, autor_id, libro_id):
    assert client.delete(f"/autores/{autor_id}").status_code == 409


def test_borra_autor_sin_libros(client, autor_id):
    assert client.delete(f"/autores/{autor_id}").status_code == 204