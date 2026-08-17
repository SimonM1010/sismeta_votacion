"""Implementacion SQLAlchemy del repositorio de usuarios."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        model = UserModel(
            username=user.username,
            hashed_password=user.hashed_password,
        )
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return _to_entity(model)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(UserModel).where(UserModel.username == username)
        model = self._session.scalar(stmt)
        return _to_entity(model) if model else None


def _to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        username=model.username,
        hashed_password=model.hashed_password,
    )
