"""Contratos de entrada/salida del modulo de autenticacion."""

from pydantic import BaseModel, ConfigDict, Field


class UserCreateDTO(BaseModel):
    """Body de POST /auth/register."""

    username: str = Field(..., min_length=3, max_length=50, examples=["admin"])
    password: str = Field(..., min_length=6, max_length=72, examples=["admin123"])


class UserResponseDTO(BaseModel):
    """Representacion publica de un usuario (nunca expone el hash)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class TokenDTO(BaseModel):
    """Respuesta de POST /auth/login."""

    access_token: str
    token_type: str = "bearer"
