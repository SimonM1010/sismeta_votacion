"""Contratos de entrada/salida del modulo de votos y estadisticas."""

from pydantic import BaseModel, ConfigDict, Field


class VoteCreateDTO(BaseModel):
    """Body de POST /votes."""

    voter_id: int = Field(..., gt=0, examples=[1])
    candidate_id: int = Field(..., gt=0, examples=[1])


class VoteResponseDTO(BaseModel):
    """Representacion publica de un voto emitido."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    voter_id: int
    candidate_id: int


class CandidateResultDTO(BaseModel):
    """Resultado individual de un candidato dentro de las estadisticas."""

    candidate_id: int
    candidate_name: str
    votes: int
    percentage: float


class VoteStatisticsDTO(BaseModel):
    """Respuesta de GET /votes/statics."""

    total_votes: int
    total_voters: int
    total_candidates: int
    participation_percentage: float
    results: list[CandidateResultDTO]
