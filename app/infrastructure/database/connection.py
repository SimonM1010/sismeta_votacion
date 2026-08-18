"""Conexion a MySQL: engine, sesiones y creacion de tablas.

El engine es perezoso: crearlo no abre ninguna conexion, por lo que la API
levanta aunque MySQL todavia no este disponible.
"""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # descarta conexiones muertas antes de usarlas
    pool_recycle=3600,  # MySQL cierra las conexiones ociosas (wait_timeout)
    echo=False,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Clase base declarativa de todos los modelos ORM."""


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: entrega una sesion y la cierra siempre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> bool:
    """Crea las tablas que aun no existan.

    No interrumpe el arranque si la base no responde: solo lo registra, para
    que puedas revisar la estructura de la API sin MySQL levantado.
    """
    # El import registra los modelos en Base.metadata antes de create_all.
    from app.infrastructure.database import models  # noqa: F401

    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        # Se registra el error completo: un CREATE TABLE puede fallar por una FK
        # incompatible y dejar la base a medias, no solo por falta de conexion.
        logger.warning(
            "Fallo la creacion de tablas (%s): %s. "
            "La API arranca igual, pero los endpoints con base de datos fallaran.",
            exc._class.name_,
            exc,
        )
        return False

    faltantes = sorted(set(Base.metadata.tables) - set(inspect(engine).get_table_names()))
    if faltantes:
        logger.error(
            "Faltan tablas en '%s': %s. Los endpoints que las usen fallaran.",
            settings.DB_DATABASE,
            ", ".join(faltantes),
        )
        return False

    logger.info("Tablas verificadas/creadas en '%s'", settings.DB_DATABASE)
    return True