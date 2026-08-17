"""Entidad de dominio: Voto.

Un voto relaciona a un votante con un candidato. Esos dos campos son el
minimo necesario para que el modulo de votos y sus estadisticas funcionen.
"""

from dataclasses import dataclass


@dataclass
class Vote:
    voter_id: int
    candidate_id: int
    id: int | None = None
