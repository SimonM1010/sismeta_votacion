"""Contratos de entrada/salida del modulo de votantes."""

from pydantic import BaseModel, ConfigDict, Field


class VoterCreateDTO(BaseModel):
    """Body de POST /voters."""

    name: str = Field(..., min_length=1, max_length=150, examples=["Juan Perez"])
    email: str = Field(..., min_length=5, max_length=150, examples=["exam@gmail.com"])


class VoterResponseDTO(BaseModel):
    """Representacion publica de un votante."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    has_voted:bool
