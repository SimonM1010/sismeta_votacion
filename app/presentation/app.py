"""Composicion de la aplicacion FastAPI.

Aqui se arma todo: routers, middlewares, manejo de errores y ciclo de vida.
Es el unico archivo que "sabe" que el framework web es FastAPI.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.config import settings
from app.domain.exceptions import AuthenticationError, ConflictError, NotFoundError
from app.infrastructure.database.connection import init_db
from app.presentation.api.v1.router import api_router

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Arranque y apagado de la aplicacion."""
    logger.info("Iniciando %s v%s", settings.PROJECT_NAME, settings.VERSION)
    init_db()
    yield
    logger.info("Apagando %s", settings.PROJECT_NAME)


def create_app() -> FastAPI:
    """Factory de la aplicacion (facilita crear instancias limpias en tests)."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=(
            "API de votaciones con arquitectura limpia. "
            "Autenticacion JWT: obtene el token en POST /auth/login y usalo "
            "con el boton Authorize."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # Abierto en desarrollo. Restringi los origenes antes de salir a produccion.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _register_exception_handlers(app)

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["Diagnostico"], summary="Informacion de la API")
    def root() -> dict:
        return {
            "project": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
            "api": settings.API_V1_PREFIX,
        }

    return app


def _register_exception_handlers(app: FastAPI) -> None:
    """Traduce errores de negocio y de base de datos a respuestas HTTP."""

    @app.exception_handler(NotFoundError)
    async def _not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    @app.exception_handler(ConflictError)
    async def _conflict(_: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": exc.message},
        )

    @app.exception_handler(AuthenticationError)
    async def _unauthorized(_: Request, exc: AuthenticationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(IntegrityError)
    async def _integrity(_: Request, exc: IntegrityError) -> JSONResponse:
        # Ej: dos votos simultaneos del mismo votante chocan con el UNIQUE.
        logger.warning("Violacion de integridad: %s", exc.orig)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "La operacion viola una restriccion de la base de datos"},
        )

    @app.exception_handler(SQLAlchemyError)
    async def _database_error(_: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.error("Error de base de datos: %s", exc, exc_info=settings.DEBUG)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "No hay conexion con la base de datos"},
        )
