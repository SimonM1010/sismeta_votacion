"""Primitivas de seguridad: hashing de contrasenas y emision/lectura de JWT.

Modulo puro: no conoce FastAPI ni la base de datos, por lo que se puede
testear en aislamiento y reutilizar desde cualquier capa.
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings

# bcrypt solo considera los primeros 72 bytes de la contrasena.
_BCRYPT_MAX_BYTES = 72


def _encode(password: str) -> bytes:
    return password.encode("utf-8")[:_BCRYPT_MAX_BYTES]


def hash_password(password: str) -> str:
    """Devuelve el hash bcrypt de una contrasena en texto plano."""
    return bcrypt.hashpw(_encode(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara una contrasena en texto plano contra su hash almacenado."""
    try:
        return bcrypt.checkpw(_encode(plain_password), hashed_password.encode("utf-8"))
    except ValueError:
        # Hash con formato invalido o corrupto.
        return False


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """Genera un JWT firmado cuyo `sub` identifica al usuario autenticado."""
    minutes = expires_minutes or settings.JWT_EXPIRE_MINUTES
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Valida firma y expiracion del token y devuelve su payload.

    Raises:
        jwt.PyJWTError: si el token es invalido, esta expirado o fue alterado.
    """
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
