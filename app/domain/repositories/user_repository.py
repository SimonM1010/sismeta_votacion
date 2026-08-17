"""Puerto (interfaz) del repositorio de usuarios."""

from abc import ABC, abstractmethod

from app.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        """Usuario nuevo y devuelve la entidad con su Id"""

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        """Busca un usuario por su nombre de usuario"""
