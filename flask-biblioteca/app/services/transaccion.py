from contextlib import contextmanager

from app.extensions import db


@contextmanager
def transaccion():
    """Todo lo que pase dentro del `with` se guarda junto, o no se guarda nada."""
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
