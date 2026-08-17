"""Puerto (interfaz) del repositorio de votantes"""

from abc import ABC, abstractmethod

from app.domain.entities.voter import Voter


class VoterRepository(ABC):
    @abstractmethod
    def create(self, voter: Voter) -> Voter:
        """Persiste un votante nuevo y devuelve la entidad con su Id"""

    @abstractmethod
    def get_all(self) -> list[Voter]:
        """Devuelve todos los votantes registrados"""

    @abstractmethod
    def get_by_id(self, voter_id: int) -> Voter | None:
        """Devuelve un votante por su Id, o None si no existe"""

    @abstractmethod
    def delete(self, voter_id: int) -> bool:
        """Elimina un votante. Devuelve False si no existia"""

    @abstractmethod
    def count(self) -> int:
        """Total de votantes registrados (usado en estadisticas)"""
