"""Entidad de dominio: Candidato.

Objeto plano, sin dependencias de SQLAlchemy ni de Pydantic.
Agrega aqui los atributos que necesites; el resto de capas los propaga.
"""

from dataclasses import dataclass


@dataclass
class Candidate:
    name: str
    id: int | None = None
    party:str
    votes:int| None = None
