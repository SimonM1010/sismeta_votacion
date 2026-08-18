"""Entidad de dominio: Votante."""

from dataclasses import dataclass


@dataclass
class Voter:
    name: str
    id: int | None = None
    email: str| None = None
    has_voted:bool| None = None
