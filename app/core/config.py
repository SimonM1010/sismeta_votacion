"""Configuracion centralizada de la aplicacion.

Todo lo que sea entorno-dependiente (credenciales, secretos, hosts) se lee
desde el archivo .env. Ninguna otra capa debe leer os.environ directamente.
"""

from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables de entorno tipadas y validadas."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    

    # --- Aplicacion ---
    PROJECT_NAME: str = "Sistema de Votaciones API"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # --- Base de datos (MySQL) ---
    DB_USER: str = "root"
    DB_PASS: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_DATABASE: str = "votacion"
    DB_CHARSET: str = "utf8mb4"

    # --- Seguridad / JWT ---
    JWT_SECRET_KEY: str = "cambiame-por-una-clave-larga-y-aleatoria"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    @field_validator("DB_PORT", mode="before")
    @classmethod
    def _blank_port_is_default(cls, value: object) -> object:
        """DB_PORT vacio en el .env significa "el puerto estandar de MySQL"."""
        if isinstance(value, str) and not value.strip():
            return 3306
        return value

    @property
    def database_url(self) -> str:
        """URL de SQLAlchemy hacia MySQL (driver PyMySQL).

        Usuario y contrasena se codifican con quote_plus: asi los simbolos
        habituales en las contrasenas (@, :, /, #) viajan escapados y no rompen
        el parseo de la URL.
        """
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASS)
        credentials = f"{user}:{password}" if password else user

        return (
            f"mysql+pymysql://{credentials}@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.DB_DATABASE}?charset={self.DB_CHARSET}"
        )


@lru_cache
def get_settings() -> Settings:
    """Instancia unica de configuracion (se cachea en el primer acceso)."""
    return Settings()


settings = get_settings()