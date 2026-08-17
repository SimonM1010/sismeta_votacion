"""Modelo ORM de la tabla Vote.

VoterId es UNIQUE: la base garantiza "un votante, un voto" aunque lleguen
dos peticiones simultaneas. Si no quieres esa regla, quita el UniqueConstraint.
"""

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class VoteModel(Base):
    __tablename__ = "Vote"
    __table_args__ = (UniqueConstraint("VoterId", name="UQ_Vote_VoterId"),)

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    voter_id: Mapped[int] = mapped_column(
        "VoterId", Integer, ForeignKey("Voter.Id"), nullable=False
    )
    candidate_id: Mapped[int] = mapped_column(
        "CandidateId", Integer, ForeignKey("Candidate.Id"), nullable=False
    )
