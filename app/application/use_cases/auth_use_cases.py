"""Casos de uso de autenticacion: registro de usuario y emision de JWT."""

from app.application.dto.auth_dto import TokenDTO, UserCreateDTO
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.entities.user import User
from app.domain.exceptions import AuthenticationError, ConflictError
from app.domain.repositories.user_repository import UserRepository


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, data: UserCreateDTO) -> User:
        if self._repository.get_by_username(data.username) is not None:
            raise ConflictError(f"El usuario '{data.username}' ya existe")

        return self._repository.create(
            User(
                username=data.username,
                hashed_password=hash_password(data.password),
            )
        )


class LoginUserUseCase:
    """Valida credenciales y devuelve el access token."""

    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, username: str, password: str) -> TokenDTO:
        user = self._repository.get_by_username(username)

        # Mismo mensaje para usuario inexistente y password incorrecto:
        # no se le revela a un atacante que usuarios existen.
        if user is None or not verify_password(password, user.hashed_password):
            raise AuthenticationError("Usuario o contrasena incorrectos")

        return TokenDTO(access_token=create_access_token(subject=user.username))
