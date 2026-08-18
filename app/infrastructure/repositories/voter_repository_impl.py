"""Implementacion SQLAlchemy del repositorio de votantes."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities.voter import Voter
from app.domain.repositories.voter_repository import VoterRepository
from app.infrastructure.database.models.voter_model import VoterModel


class SqlAlchemyVoterRepository(VoterRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, voter: Voter) -> Voter:
        model = VoterModel(name=voter.name,email=voter.email)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return _to_entity(model)

    def get_all(self) -> list[Voter]:
        models = self._session.scalars(
            select(VoterModel).order_by(VoterModel.id)
        ).all()
        return [_to_entity(model) for model in models]

    def get_by_id(self, voter_id: int) -> Voter | None:
        model = self._session.get(VoterModel, voter_id)
        return _to_entity(model) if model else None

    def delete(self, voter_id: int) -> bool:
        model = self._session.get(VoterModel, voter_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.commit()
        return True

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(VoterModel)) or 0

    def update_hasvoted(self,voter_id:int)-> bool:
        model = self._session.get(VoterModel, voter_id)
    
        if model is None:
            return False

        model.has_voted = True
        self._session.commit()

        return True


def _to_entity(model: VoterModel) -> Voter:
    return Voter(id=model.id, name=model.name,email=model.email,has_voted=model.has_voted)
