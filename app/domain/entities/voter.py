"""Entidad de dominio: Votante."""

from dataclasses import dataclass


@dataclass
class Voter:
    name: str
    id: int | None = None
