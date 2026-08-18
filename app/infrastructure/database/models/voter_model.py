"""Modelo ORM de la tabla Voter.

Base minima: Id y Name. Agrega aqui las columnas que falten
(documento, correo, mesa, etc.).
"""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class VoterModel(Base):
    __tablename__ = "Voter"

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("Name", String(150), nullable=False)
    email: Mapped[str] = mapped_column("email", String(150), nullable=False)
    has_voted:Mapped[bool] = mapped_column("has_voted", Boolean, default=False, nullable=False)