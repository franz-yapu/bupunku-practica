from contextlib import contextmanager
from app.extensions import db

@contextmanager
def transaccion():
    """Context manager para manejar transacciones de base de datos.
    Si ocurre una excepción dentro del bloque 'with', la transacción se revierte.
    """
    try:
        yield
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e