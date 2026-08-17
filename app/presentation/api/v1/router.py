"""Agregador de routers de la version 1 de la API."""

from fastapi import APIRouter

from app.presentation.api.v1.endpoints import auth, candidates, health, voters, votes

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(voters.router)
api_router.include_router(candidates.router)
api_router.include_router(votes.router)
