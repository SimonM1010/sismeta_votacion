"""Entidad de dominio: Votante."""

from dataclasses import dataclass


@dataclass
class Voter:
    email: str
    name: str
    id: int | None = None
    has_voted:bool=False
