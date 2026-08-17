"""Endpoints del modulo de candidatos (todos requieren JWT)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.application.dto.candidate_dto import CandidateCreateDTO, CandidateResponseDTO
from app.application.use_cases.candidate_use_cases import (
    CreateCandidateUseCase,
    DeleteCandidateUseCase,
    GetCandidateUseCase,
    ListCandidatesUseCase,
)
from app.presentation.api.dependencies import (
    get_create_candidate_use_case,
    get_current_user,
    get_delete_candidate_use_case,
    get_get_candidate_use_case,
    get_list_candidates_use_case,
)

router = APIRouter(
    prefix="/candidates",
    tags=["Candidatos"],
    dependencies=[Depends(get_current_user)],
)

CandidateId = Annotated[int, Path(gt=0, description="Id del candidato")]


@router.post(
    "",
    response_model=CandidateResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un candidato nuevo",
)
def create_candidate(
    payload: CandidateCreateDTO,
    use_case: Annotated[CreateCandidateUseCase, Depends(get_create_candidate_use_case)],
) -> CandidateResponseDTO:
    return CandidateResponseDTO.model_validate(use_case.execute(payload))


@router.get(
    "",
    response_model=list[CandidateResponseDTO],
    summary="Obtener la lista de candidatos",
)
def list_candidates(
    use_case: Annotated[ListCandidatesUseCase, Depends(get_list_candidates_use_case)],
) -> list[CandidateResponseDTO]:
    return [CandidateResponseDTO.model_validate(item) for item in use_case.execute()]


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponseDTO,
    summary="Obtener un candidato por su Id",
)
def get_candidate(
    candidate_id: CandidateId,
    use_case: Annotated[GetCandidateUseCase, Depends(get_get_candidate_use_case)],
) -> CandidateResponseDTO:
    return CandidateResponseDTO.model_validate(use_case.execute(candidate_id))


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un candidato",
)
def delete_candidate(
    candidate_id: CandidateId,
    use_case: Annotated[DeleteCandidateUseCase, Depends(get_delete_candidate_use_case)],
) -> None:
    use_case.execute(candidate_id)
