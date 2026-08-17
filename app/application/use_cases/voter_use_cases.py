"""Casos de uso del modulo de votantes."""

from app.application.dto.voter_dto import VoterCreateDTO
from app.domain.entities.voter import Voter
from app.domain.exceptions import ConflictError, NotFoundError
from app.domain.repositories.vote_repository import VoteRepository
from app.domain.repositories.voter_repository import VoterRepository


class CreateVoterUseCase:
    def __init__(self, repository: VoterRepository) -> None:
        self._repository = repository

    def execute(self, data: VoterCreateDTO) -> Voter:
        return self._repository.create(Voter(name=data.name))


class ListVotersUseCase:
    def __init__(self, repository: VoterRepository) -> None:
        self._repository = repository

    def execute(self) -> list[Voter]:
        return self._repository.get_all()


class GetVoterUseCase:
    def __init__(self, repository: VoterRepository) -> None:
        self._repository = repository

    def execute(self, voter_id: int) -> Voter:
        voter = self._repository.get_by_id(voter_id)
        if voter is None:
            raise NotFoundError(f"No existe el votante con id {voter_id}")
        return voter


class DeleteVoterUseCase:
    """Elimina un votante que todavia no haya votado.

    Borrarlo despues de votar dejaria su voto huerfano y descuadraria el
    conteo, asi que se bloquea. Si prefieres borrado en cascada, elimina la
    verificacion y agrega ON DELETE CASCADE a la FK de Vote.
    """

    def __init__(
        self,
        repository: VoterRepository,
        vote_repository: VoteRepository,
    ) -> None:
        self._repository = repository
        self._votes = vote_repository

    def execute(self, voter_id: int) -> None:
        if self._repository.get_by_id(voter_id) is None:
            raise NotFoundError(f"No existe el votante con id {voter_id}")

        if self._votes.exists_by_voter(voter_id):
            raise ConflictError(
                f"No se puede eliminar el votante {voter_id}: ya emitio su voto"
            )

        self._repository.delete(voter_id)
