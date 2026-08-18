"""Casos de uso del modulo de candidatos.

Cada clase encapsula una unica operacion del negocio y depende solo del
puerto CandidateRepository, nunca de SQLAlchemy ni de FastAPI.
"""

from app.application.dto.candidate_dto import CandidateCreateDTO
from app.domain.entities.candidate import Candidate
from app.domain.exceptions import ConflictError, NotFoundError
from app.domain.repositories.candidate_repository import CandidateRepository
from app.domain.repositories.vote_repository import VoteRepository


class CreateCandidateUseCase:
    def __init__(self, repository: CandidateRepository) -> None:
        self._repository = repository

    def execute(self, data: CandidateCreateDTO) -> Candidate:
        return self._repository.create(Candidate(name=data.name,party=data.party))


class ListCandidatesUseCase:
    def __init__(self, repository: CandidateRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Candidate]:
        return self._repository.get_all()


class GetCandidateUseCase:
    def __init__(self, repository: CandidateRepository) -> None:
        self._repository = repository

    def execute(self, candidate_id: int) -> Candidate:
        candidate = self._repository.get_by_id(candidate_id)
        if candidate is None:
            raise NotFoundError(f"No existe el candidato con id {candidate_id}")
        return candidate


class DeleteCandidateUseCase:
    """Elimina un candidato que todavia no haya recibido votos.

    Borrarlo despues de recibir votos dejaria esos votos huerfanos y
    descuadraria el conteo, asi que se bloquea.
    """

    def __init__(
        self,
        repository: CandidateRepository,
        vote_repository: VoteRepository,
    ) -> None:
        self._repository = repository
        self._votes = vote_repository

    def execute(self, candidate_id: int) -> None:
        if self._repository.get_by_id(candidate_id) is None:
            raise NotFoundError(f"No existe el candidato con id {candidate_id}")

        if self._votes.exists_by_candidate(candidate_id):
            raise ConflictError(
                f"No se puede eliminar el candidato {candidate_id}: ya tiene votos"
            )

        self._repository.delete(candidate_id)
