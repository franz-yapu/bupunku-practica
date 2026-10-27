from datetime import date

import pytest

from app import create_app, db


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()


# --- helpers ---

def crear_autor(client, nombre="Borges"):
    resp = client.post("/autores", json={"nombre": nombre})
    return resp.get_json()["id"]


def crear_libro(client, autor_id, **extra):
    datos = {"titulo": "Ficciones", "anio": 1944, "autor_id": autor_id, **extra}
    return client.post("/libros", json=datos)


# --- tests ---

def test_crear_autor_sin_nombre_da_400(client):
    resp = client.post("/autores", json={"pais": "Chile"})
    assert resp.status_code == 400


def test_crear_libro_ok_disponible_por_defecto(client):
    autor_id = crear_autor(client)
    resp = crear_libro(client, autor_id)
    assert resp.status_code == 201
    assert resp.get_json()["disponible"] is True


def test_crear_libro_con_autor_inexistente_da_404(client):
    resp = crear_libro(client, 999)
    assert resp.status_code == 404


def test_crear_libro_con_anio_futuro_da_422(client):
    autor_id = crear_autor(client)
    resp = crear_libro(client, autor_id, anio=date.today().year + 1)
    assert resp.status_code == 422


def test_patch_actualiza_solo_lo_enviado(client):
    autor_id = crear_autor(client)
    libro_id = crear_libro(client, autor_id).get_json()["id"]

    resp = client.patch(f"/libros/{libro_id}", json={"disponible": False})

    assert resp.status_code == 200
    datos = resp.get_json()
    assert datos["disponible"] is False
    assert datos["titulo"] == "Ficciones"   # no se tocó
    assert datos["anio"] == 1944            # no se tocó


def test_filtro_disponible(client):
    autor_id = crear_autor(client)
    crear_libro(client, autor_id, titulo="A")
    crear_libro(client, autor_id, titulo="B", disponible=False)

    resp = client.get("/libros?disponible=true")

    titulos = [l["titulo"] for l in resp.get_json()["items"]]
    assert titulos == ["A"]


def test_borrar_autor_con_libros_da_409_y_sin_libros_204(client):
    con_libros = crear_autor(client, "Borges")
    crear_libro(client, con_libros)
    sin_libros = crear_autor(client, "Cortázar")

    assert client.delete(f"/autores/{con_libros}").status_code == 409
    assert client.delete(f"/autores/{sin_libros}").status_code == 204


def test_libros_de_autor_inexistente_da_404_en_json(client):
    resp = client.get("/autores/999/libros")
    assert resp.status_code == 404
    assert resp.is_json


def test_ruta_inexistente_da_404_en_json(client):
    resp = client.get("/no-existe")
    assert resp.status_code == 404
    assert resp.is_json


def test_paginacion_autores(client):
    for i in range(12):
        crear_autor(client, f"Autor {i}")

    resp = client.get("/autores?pagina=2")

    datos = resp.get_json()
    assert datos["total"] == 12
    assert len(datos["items"]) == 2