def test_prestar_marca_el_libro_como_no_disponible(client, libro_id, socio_id):
    r = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id})
    assert r.status_code == 201

    libros = client.get("/libros?disponible=false").get_json()["items"]
    assert [l["id"] for l in libros] == [libro_id]


def test_no_se_presta_un_libro_ya_prestado(client, libro_id, socio_id):
    client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id})
    r = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id})
    assert r.status_code == 409


def test_devolver_libera_el_libro(client, libro_id, socio_id):
    prestamo = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id}).get_json()

    r = client.post(f"/prestamos/{prestamo['id']}/devolver")

    assert r.status_code == 200
    assert r.get_json()["fecha_devolucion"] is not None
    assert client.get("/libros?disponible=true").get_json()["items"][0]["id"] == libro_id


def test_devolver_dos_veces_da_409(client, libro_id, socio_id):
    prestamo = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": socio_id}).get_json()
    client.post(f"/prestamos/{prestamo['id']}/devolver")
    assert client.post(f"/prestamos/{prestamo['id']}/devolver").status_code == 409


def test_socio_inexistente_no_cambia_el_libro(client, libro_id):
    r = client.post("/prestamos", json={"libro_id": libro_id, "socio_id": 999})
    assert r.status_code == 404
    assert client.get("/libros?disponible=true").get_json()["items"][0]["id"] == libro_id


def test_email_repetido_da_409(client, socio_id):
    r = client.post("/socios", json={"nombre": "Otra", "email": "ANA@mail.com"})
    assert r.status_code == 409