"""Modelo ORM de la tabla Candidate.

Base minima: Id y Name. Agrega aqui las columnas que falten
(partido, foto, numero de lista, etc.).
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class CandidateModel(Base):
    __tablename__ = "Candidate"

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("Name", String(150), nullable=False)
