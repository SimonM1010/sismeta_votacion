"""Puerto (interfaz) del repositorio de votos."""

from abc import ABC, abstractmethod

from app.domain.entities.vote import Vote


class VoteRepository(ABC):
    @abstractmethod
    def create(self, vote: Vote) -> Vote:
        """Registra un voto y devuelve la entidad con su Id"""

    @abstractmethod
    def get_all(self) -> list[Vote]:
        """Devuelve todos los votos emitidos"""

    @abstractmethod
    def exists_by_voter(self, voter_id: int) -> bool:
        """Indica si el votante ya emitio su voto"""

    @abstractmethod
    def exists_by_candidate(self, candidate_id: int) -> bool:
        """Indica si el candidato ya recibio algun voto"""

    @abstractmethod
    def count(self) -> int:
        """Total de votos emitidos."""

    @abstractmethod
    def count_by_candidate(self) -> dict[int, int]:
        """Votos agrupados por candidato: {candidate_id: total}"""
