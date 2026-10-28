class ErrorDeNegocio(Exception):
    """Base de todos los errores que el negocio puede lanzar. No sabe nada de HTTP."""

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje


class DatosInvalidos(ErrorDeNegocio):
    pass


class NoEncontrado(ErrorDeNegocio):
    pass


class Conflicto(ErrorDeNegocio):
    pass


class ReglaDeNegocio(ErrorDeNegocio):
    pass
