"""Modelo ORM de la tabla Users (credenciales para el JWT).

Se llama "Users" y no "User" porque USER es palabra reservada en T-SQL.
Solo se guarda el hash bcrypt, nunca la contrasena en texto plano.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column("Id", Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        "Username", String(50), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(
        "HashedPassword", String(255), nullable=False
    )
