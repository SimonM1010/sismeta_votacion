"""Entidad de dominio: Candidato.

Objeto plano, sin dependencias de SQLAlchemy ni de Pydantic.
Agrega aqui los atributos que necesites; el resto de capas los propaga.
"""

from dataclasses import dataclass


@dataclass
class Candidate:
    name: str
    party:str
    id: int | None = None
    votes:int = 0
