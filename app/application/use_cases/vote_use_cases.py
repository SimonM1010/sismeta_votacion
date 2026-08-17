"""Casos de uso del modulo de votos.

Aqui viven las reglas de negocio de la votacion:
  - el votante y el candidato deben existir,
  - un votante solo puede emitir un voto.
"""

from app.application.dto.vote_dto import (
    CandidateResultDTO,
    VoteCreateDTO,
    VoteStatisticsDTO,
)
from app.domain.entities.vote import Vote
from app.domain.exceptions import ConflictError, NotFoundError
from app.domain.repositories.candidate_repository import CandidateRepository
from app.domain.repositories.vote_repository import VoteRepository
from app.domain.repositories.voter_repository import VoterRepository


class CastVoteUseCase:
    """Emite un voto validando las reglas del negocio."""

    def __init__(
        self,
        vote_repository: VoteRepository,
        voter_repository: VoterRepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self._votes = vote_repository
        self._voters = voter_repository
        self._candidates = candidate_repository

    def execute(self, data: VoteCreateDTO) -> Vote:
        if self._voters.get_by_id(data.voter_id) is None:
            raise NotFoundError(f"No existe el votante con id {data.voter_id}")

        if self._candidates.get_by_id(data.candidate_id) is None:
            raise NotFoundError(f"No existe el candidato con id {data.candidate_id}")

        if self._votes.exists_by_voter(data.voter_id):
            raise ConflictError(
                f"El votante con id {data.voter_id} ya emitio su voto"
            )

        return self._votes.create(
            Vote(voter_id=data.voter_id, candidate_id=data.candidate_id)
        )


class ListVotesUseCase:
    def __init__(self, vote_repository: VoteRepository) -> None:
        self._votes = vote_repository

    def execute(self) -> list[Vote]:
        return self._votes.get_all()


class GetVoteStatisticsUseCase:
    """Calcula el resumen de la votacion: totales, participacion y ranking."""

    def __init__(
        self,
        vote_repository: VoteRepository,
        voter_repository: VoterRepository,
        candidate_repository: CandidateRepository,
    ) -> None:
        self._votes = vote_repository
        self._voters = voter_repository
        self._candidates = candidate_repository

    def execute(self) -> VoteStatisticsDTO:
        candidates = self._candidates.get_all()
        votes_by_candidate = self._votes.count_by_candidate()
        total_votes = self._votes.count()
        total_voters = self._voters.count()

        results = [
            CandidateResultDTO(
                candidate_id=candidate.id,
                candidate_name=candidate.name,
                votes=votes_by_candidate.get(candidate.id, 0),
                percentage=_percentage(
                    votes_by_candidate.get(candidate.id, 0), total_votes
                ),
            )
            for candidate in candidates
        ]
        results.sort(key=lambda result: result.votes, reverse=True)

        return VoteStatisticsDTO(
            total_votes=total_votes,
            total_voters=total_voters,
            total_candidates=len(candidates),
            participation_percentage=_percentage(total_votes, total_voters),
            results=results,
        )


def _percentage(part: int, total: int) -> float:
    """Porcentaje redondeado a 2 decimales, tolerante a total = 0."""
    if total <= 0:
        return 0.0
    return round(part * 100 / total, 2)
