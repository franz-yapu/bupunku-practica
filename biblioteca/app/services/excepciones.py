class ErrorDeNegocion(Exception):
    """Clase base para las excepciones de denegación de acceso. NO sabe nada de http, solo es un error de negocio"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

class DataInvalidaError(ErrorDeNegocion):
    """Excepción para datos inválidos"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        super().__init__(mensaje)

class DataInvalidos(ErrorDeNegocion):
    """Excepción para datos inválidos"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        super().__init__(mensaje)
class NoEncontradoError(ErrorDeNegocion):
    """Excepción para datos inválidos"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        super().__init__(mensaje)

class conflictoError(ErrorDeNegocion):
    """Excepción para datos inválidos"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        super().__init__(mensaje)

class ReglaDeNegocioError(ErrorDeNegocion):
    """Excepción para datos inválidos"""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        super().__init__(mensaje)