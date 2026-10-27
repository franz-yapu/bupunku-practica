"""Validación de FORMATO: ¿llegó el dato? ¿es del tipo correcto? ¿cabe en la columna?
Las reglas de NEGOCIO (año futuro, libro prestado...) viven en los servicios."""

from flask import request

from app.services.excepciones import DataInvalidos


def leer_json():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise DataInvalidos("Se esperaba un objeto JSON")
    return datos


def texto(datos, campo, max_largo, obligatorio=True):
    valor = datos.get(campo)
    if valor is None and not obligatorio:
        return None
    if not isinstance(valor, str) or not valor.strip():
        raise DataInvalidos(f"'{campo}' es obligatorio y debe ser texto")
    valor = valor.strip()
    if len(valor) > max_largo:
        raise DataInvalidos(f"'{campo}' admite como máximo {max_largo} caracteres")
    return valor


def entero(datos, campo, obligatorio=True):
    valor = datos.get(campo)
    if valor is None and not obligatorio:
        return None
    # En Python, True es un int: hay que excluir bool a mano
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise DataInvalidos(f"'{campo}' debe ser un número entero")
    return valor


def booleano(datos, campo, por_defecto):
    valor = datos.get(campo, por_defecto)
    if not isinstance(valor, bool):
        raise DataInvalidos(f"'{campo}' debe ser true o false")
    return valor


def pagina_de_query():
    pagina = request.args.get("pagina", 1, type=int)
    if pagina < 1:
        raise DataInvalidos("'pagina' debe ser 1 o mayor")
    return pagina