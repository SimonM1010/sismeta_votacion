"""Endpoints de autenticacion.

/auth/login es el unico endpoint publico del sistema.

/auth/register queda abierto para poder crear el primer usuario (si no,
no habria forma de obtener un token). Cuando ya tengas tu admin creado,
protegelo agregando `current_user: CurrentUser` a la firma.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.dto.auth_dto import TokenDTO, UserCreateDTO, UserResponseDTO
from app.application.use_cases.auth_use_cases import (
    LoginUserUseCase,
    RegisterUserUseCase,
)
from app.presentation.api.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
)

router = APIRouter(prefix="/auth", tags=["Autenticacion"])


@router.post(
    "/register",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un usuario del sistema",
)
def register(
    payload: UserCreateDTO,
    use_case: Annotated[RegisterUserUseCase, Depends(get_register_user_use_case)],
) -> UserResponseDTO:
    user = use_case.execute(payload)
    return UserResponseDTO.model_validate(user)


@router.post(
    "/login",
    response_model=TokenDTO,
    summary="Obtener el access token (JWT)",
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: Annotated[LoginUserUseCase, Depends(get_login_user_use_case)],
) -> TokenDTO:
    """Recibe usuario/contrasena como formulario y devuelve el Bearer token.

    Usar el boton **Authorize** de /docs completa este flujo automaticamente.
    """
    return use_case.execute(form_data.username, form_data.password)
