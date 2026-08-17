"""Endpoint de diagnostico: sirve para confirmar que la API y la base responden."""

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.infrastructure.database.connection import engine

router = APIRouter(tags=["Diagnostico"])


@router.get("/health", summary="Estado de la API y de la base de datos")
def health() -> dict:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        database_status = "ok"
    except SQLAlchemyError as exc:
        database_status = f"error: {exc.__class__.__name__}"

    return {
        "api": "ok",
        "database": database_status,
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }
