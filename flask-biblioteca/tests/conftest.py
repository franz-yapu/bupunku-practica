import pytest

from app import create_app
from app.extensions import db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def autor_id(client):
    return client.post("/autores", json={"nombre": "Borges"}).get_json()["id"]


@pytest.fixture
def libro_id(client, autor_id):
    r = client.post("/libros", json={"titulo": "Ficciones", "anio": 1944, "autor_id": autor_id})
    return r.get_json()["id"]


@pytest.fixture
def socio_id(client):
    return client.post("/socios", json={"nombre": "Ana", "email": "ana@mail.com"}).get_json()["id"]
