"""Inyeccion de dependencias de la API.

Este es el unico punto donde se decide que implementacion concreta recibe
cada caso de uso. Cambiar SQL Server por otro motor se hace aqui, sin tocar
ni el dominio ni los casos de uso.
"""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.application.use_cases.auth_use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
)
from app.application.use_cases.candidate_use_cases import (
    CreateCandidateUseCase,
    DeleteCandidateUseCase,
    GetCandidateUseCase,
    ListCandidatesUseCase,
)
from app.application.use_cases.vote_use_cases import (
    CastVoteUseCase,
    GetVoteStatisticsUseCase,
    ListVotesUseCase,
)
from app.application.use_cases.voter_use_cases import (
    CreateVoterUseCase,
    DeleteVoterUseCase,
    GetVoterUseCase,
    ListVotersUseCase,
)
from app.core.config import settings
from app.core.security import decode_access_token
from app.domain.entities.user import User
from app.domain.repositories.candidate_repository import CandidateRepository
from app.domain.repositories.user_repository import UserRepository
from app.domain.repositories.vote_repository import VoteRepository
from app.domain.repositories.voter_repository import VoterRepository
from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.candidate_repository_impl import (
    SqlAlchemyCandidateRepository,
)
from app.infrastructure.repositories.user_repository_impl import (
    SqlAlchemyUserRepository,
)
from app.infrastructure.repositories.vote_repository_impl import (
    SqlAlchemyVoteRepository,
)
from app.infrastructure.repositories.voter_repository_impl import (
    SqlAlchemyVoterRepository,
)

# ---------------------------------------------------------------- sesion ---

DbSession = Annotated[Session, Depends(get_db)]


# ----------------------------------------------------------- repositorios ---


def get_candidate_repository(db: DbSession) -> CandidateRepository:
    return SqlAlchemyCandidateRepository(db)


def get_voter_repository(db: DbSession) -> VoterRepository:
    return SqlAlchemyVoterRepository(db)


def get_vote_repository(db: DbSession) -> VoteRepository:
    return SqlAlchemyVoteRepository(db)


def get_user_repository(db: DbSession) -> UserRepository:
    return SqlAlchemyUserRepository(db)


CandidateRepo = Annotated[CandidateRepository, Depends(get_candidate_repository)]
VoterRepo = Annotated[VoterRepository, Depends(get_voter_repository)]
VoteRepo = Annotated[VoteRepository, Depends(get_vote_repository)]
UserRepo = Annotated[UserRepository, Depends(get_user_repository)]


# ------------------------------------------------------- casos de uso: candidatos ---


def get_create_candidate_use_case(repo: CandidateRepo) -> CreateCandidateUseCase:
    return CreateCandidateUseCase(repo)


def get_list_candidates_use_case(repo: CandidateRepo) -> ListCandidatesUseCase:
    return ListCandidatesUseCase(repo)


def get_get_candidate_use_case(repo: CandidateRepo) -> GetCandidateUseCase:
    return GetCandidateUseCase(repo)


def get_delete_candidate_use_case(
    repo: CandidateRepo, votes: VoteRepo
) -> DeleteCandidateUseCase:
    return DeleteCandidateUseCase(repo, votes)


# ---------------------------------------------------------- casos de uso: votantes ---


def get_create_voter_use_case(repo: VoterRepo) -> CreateVoterUseCase:
    return CreateVoterUseCase(repo)


def get_list_voters_use_case(repo: VoterRepo) -> ListVotersUseCase:
    return ListVotersUseCase(repo)


def get_get_voter_use_case(repo: VoterRepo) -> GetVoterUseCase:
    return GetVoterUseCase(repo)


def get_delete_voter_use_case(repo: VoterRepo, votes: VoteRepo) -> DeleteVoterUseCase:
    return DeleteVoterUseCase(repo, votes)


# ------------------------------------------------------------- casos de uso: votos ---


def get_cast_vote_use_case(
    votes: VoteRepo, voters: VoterRepo, candidates: CandidateRepo
) -> CastVoteUseCase:
    return CastVoteUseCase(votes, voters, candidates)


def get_list_votes_use_case(votes: VoteRepo) -> ListVotesUseCase:
    return ListVotesUseCase(votes)


def get_vote_statistics_use_case(
    votes: VoteRepo, voters: VoterRepo, candidates: CandidateRepo
) -> GetVoteStatisticsUseCase:
    return GetVoteStatisticsUseCase(votes, voters, candidates)


# ---------------------------------------------------------------- casos de uso: auth ---


def get_register_user_use_case(repo: UserRepo) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)


def get_login_user_use_case(repo: UserRepo) -> LoginUserUseCase:
    return LoginUserUseCase(repo)


# -------------------------------------------------------------------- seguridad ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    users: UserRepo,
) -> User:
    """Valida el Bearer token y devuelve el usuario autenticado."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
    except jwt.PyJWTError:
        raise credentials_error from None

    username = payload.get("sub")
    if not username:
        raise credentials_error

    user = users.get_by_username(username)
    if user is None:
        raise credentials_error

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
