"""Contratos de entrada/salida del modulo de candidatos."""

from pydantic import BaseModel, ConfigDict, Field


class CandidateCreateDTO(BaseModel):
    """Body de POST /candidates."""

    name: str = Field(..., min_length=1, max_length=150, examples=["Simon Mazo"])


class CandidateResponseDTO(BaseModel):
    """Representacion publica de un candidato."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
