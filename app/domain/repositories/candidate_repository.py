"""Puerto (interfaz) del repositorio de candidatos.

Los casos de uso dependen de esta abstraccion, nunca de SQLAlchemy.
La implementacion concreta vive en app/infrastructure/repositories/.
"""

from abc import ABC, abstractmethod

from app.domain.entities.candidate import Candidate


class CandidateRepository(ABC):
    @abstractmethod
    def create(self, candidate: Candidate) -> Candidate:
        """Candidato nuevo y devuelve la entidad con su Id"""

    @abstractmethod
    def get_all(self) -> list[Candidate]:
        """Devuelve todos los candidatos registrados"""

    @abstractmethod
    def get_by_id(self, candidate_id: int) -> Candidate | None:
        """Devuelve un candidato por su Id, o None si no existe"""

    @abstractmethod
    def delete(self, candidate_id: int) -> bool:
        """Elimina un candidato. Devuelve False si no existia"""
