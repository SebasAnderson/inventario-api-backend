from fastapi import APIRouter, status
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserResponse
from app.schemas.common import UserRole

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión (Login)",
    description="Autentica las credenciales del usuario y retorna un token JWT Bearer junto con los datos de perfil."
)
def login(credentials: LoginRequest):
    # Mock data para el contrato de la API (Sprint 4)
    mock_user = UserResponse(
        id=1,
        email=credentials.email,
        rol=UserRole.ADMIN if "admin" in credentials.email else UserRole.EMPLEADO,
        activo=True
    )
    return TokenResponse(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.contrato-sprint-4-mock-token",
        token_type="bearer",
        user=mock_user
    )
