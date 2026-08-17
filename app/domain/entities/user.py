"""Entidad de dominio: Usuario del sistema (autenticacion JWT).

Es la unica tabla que existe para emitir tokens: candidatos y votantes son
datos del negocio, no credenciales.
"""

from dataclasses import dataclass


@dataclass
class User:
    username: str
    hashed_password: str
    id: int | None = None
