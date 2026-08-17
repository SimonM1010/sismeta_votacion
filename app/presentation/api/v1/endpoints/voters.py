"""Endpoints del modulo de votantes (todos requieren JWT)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.application.dto.voter_dto import VoterCreateDTO, VoterResponseDTO
from app.application.use_cases.voter_use_cases import (
    CreateVoterUseCase,
    DeleteVoterUseCase,
    GetVoterUseCase,
    ListVotersUseCase,
)
from app.presentation.api.dependencies import (
    get_create_voter_use_case,
    get_current_user,
    get_delete_voter_use_case,
    get_get_voter_use_case,
    get_list_voters_use_case,
)

router = APIRouter(
    prefix="/voters",
    tags=["Votantes"],
    dependencies=[Depends(get_current_user)],
)

VoterId = Annotated[int, Path(gt=0, description="Id del votante")]


@router.post(
    "",
    response_model=VoterResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un votante nuevo",
)
def create_voter(
    payload: VoterCreateDTO,
    use_case: Annotated[CreateVoterUseCase, Depends(get_create_voter_use_case)],
) -> VoterResponseDTO:
    return VoterResponseDTO.model_validate(use_case.execute(payload))


@router.get(
    "",
    response_model=list[VoterResponseDTO],
    summary="Obtener la lista de votantes",
)
def list_voters(
    use_case: Annotated[ListVotersUseCase, Depends(get_list_voters_use_case)],
) -> list[VoterResponseDTO]:
    return [VoterResponseDTO.model_validate(item) for item in use_case.execute()]


@router.get(
    "/{voter_id}",
    response_model=VoterResponseDTO,
    summary="Obtener un votante por su Id",
)
def get_voter(
    voter_id: VoterId,
    use_case: Annotated[GetVoterUseCase, Depends(get_get_voter_use_case)],
) -> VoterResponseDTO:
    return VoterResponseDTO.model_validate(use_case.execute(voter_id))


@router.delete(
    "/{voter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un votante",
)
def delete_voter(
    voter_id: VoterId,
    use_case: Annotated[DeleteVoterUseCase, Depends(get_delete_voter_use_case)],
) -> None:
    use_case.execute(voter_id)
