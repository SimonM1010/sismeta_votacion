"""Punto de entrada de la API de votaciones.

Ejecutar en desarrollo:
    uvicorn main:app --reload
o simplemente:
    python main.py
"""

import uvicorn

from app.presentation.app import create_app

app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
