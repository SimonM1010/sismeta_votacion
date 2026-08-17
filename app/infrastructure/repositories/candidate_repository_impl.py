"""Implementacion SQLAlchemy del repositorio de candidatos.

Traduce entre el modelo ORM (infraestructura) y la entidad (dominio):
fuera de esta capa nadie ve un objeto de SQLAlchemy.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.candidate import Candidate
from app.domain.repositories.candidate_repository import CandidateRepository
from app.infrastructure.database.models.candidate_model import CandidateModel


class SqlAlchemyCandidateRepository(CandidateRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, candidate: Candidate) -> Candidate:
        model = CandidateModel(name=candidate.name)
        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)
        return _to_entity(model)

    def get_all(self) -> list[Candidate]:
        models = self._session.scalars(
            select(CandidateModel).order_by(CandidateModel.id)
        ).all()
        return [_to_entity(model) for model in models]

    def get_by_id(self, candidate_id: int) -> Candidate | None:
        model = self._session.get(CandidateModel, candidate_id)
        return _to_entity(model) if model else None

    def delete(self, candidate_id: int) -> bool:
        model = self._session.get(CandidateModel, candidate_id)
        if model is None:
            return False
        self._session.delete(model)
        self._session.commit()
        return True


def _to_entity(model: CandidateModel) -> Candidate:
    return Candidate(id=model.id, name=model.name)
