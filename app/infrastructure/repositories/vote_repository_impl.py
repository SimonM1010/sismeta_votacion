"""Implementacion SQLAlchemy del repositorio de votos."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.entities.vote import Vote
from app.domain.repositories.vote_repository import VoteRepository
from app.infrastructure.database.models.vote_model import VoteModel


class SqlAlchemyVoteRepository(VoteRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, vote: Vote) -> Vote:
        model = VoteModel(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return _to_entity(model)

    def get_all(self) -> list[Vote]:
        models = self._session.scalars(select(VoteModel).order_by(VoteModel.id)).all()
        return [_to_entity(model) for model in models]

    def exists_by_voter(self, voter_id: int) -> bool:
        stmt = select(VoteModel.id).where(VoteModel.voter_id == voter_id).limit(1)
        return self._session.scalar(stmt) is not None

    def exists_by_candidate(self, candidate_id: int) -> bool:
        stmt = select(VoteModel.id).where(VoteModel.candidate_id == candidate_id).limit(1)
        return self._session.scalar(stmt) is not None

    def count(self) -> int:
        return self._session.scalar(select(func.count()).select_from(VoteModel)) or 0

    def count_by_candidate(self) -> dict[int, int]:
        # Un solo GROUP BY en SQL: evita traer todos los votos a memoria.
        stmt = select(VoteModel.candidate_id, func.count(VoteModel.id)).group_by(
            VoteModel.candidate_id
        )
        return {candidate_id: total for candidate_id, total in self._session.execute(stmt)}


def _to_entity(model: VoteModel) -> Vote:
    return Vote(id=model.id, voter_id=model.voter_id, candidate_id=model.candidate_id)
