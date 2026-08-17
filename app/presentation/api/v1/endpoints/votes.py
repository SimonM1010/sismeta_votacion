"""Endpoints del modulo de votos (todos requieren JWT)."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.dto.vote_dto import (
    VoteCreateDTO,
    VoteResponseDTO,
    VoteStatisticsDTO,
)
from app.application.use_cases.vote_use_cases import (
    CastVoteUseCase,
    GetVoteStatisticsUseCase,
    ListVotesUseCase,
)
from app.presentation.api.dependencies import (
    get_cast_vote_use_case,
    get_current_user,
    get_list_votes_use_case,
    get_vote_statistics_use_case,
)

router = APIRouter(
    prefix="/votes",
    tags=["Votos"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "",
    response_model=VoteResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Emitir un voto",
)
def cast_vote(
    payload: VoteCreateDTO,
    use_case: Annotated[CastVoteUseCase, Depends(get_cast_vote_use_case)],
) -> VoteResponseDTO:
    return VoteResponseDTO.model_validate(use_case.execute(payload))


@router.get(
    "",
    response_model=list[VoteResponseDTO],
    summary="Obtener los votos emitidos",
)
def list_votes(
    use_case: Annotated[ListVotesUseCase, Depends(get_list_votes_use_case)],
) -> list[VoteResponseDTO]:
    return [VoteResponseDTO.model_validate(item) for item in use_case.execute()]


@router.get(
    "/statics",
    response_model=VoteStatisticsDTO,
    summary="Obtener estadisticas de la votacion",
)
def get_statistics(
    use_case: Annotated[GetVoteStatisticsUseCase, Depends(get_vote_statistics_use_case)],
) -> VoteStatisticsDTO:
    """Totales, porcentaje de participacion y ranking de candidatos."""
    return use_case.execute()
