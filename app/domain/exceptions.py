"""Errores de negocio.

La capa de dominio y los casos de uso lanzan estas excepciones sin saber nada
de HTTP. La capa de presentacion las traduce a codigos de estado.
"""


class DomainError(Exception):
    """Error base del dominio."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    """no existe"""


class ConflictError(DomainError):
    """estado invalido"""


class AuthenticationError(DomainError):
    """Credencial invalida"""
