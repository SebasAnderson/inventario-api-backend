from typing import List
from fastapi import APIRouter, status, Path
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.common import UserRole

router = APIRouter()

MOCK_USERS = [
    UserResponse(id=1, email="admin@comicstore.com", rol=UserRole.ADMIN, activo=True),
    UserResponse(id=2, email="empleado@comicstore.com", rol=UserRole.EMPLEADO, activo=True),
    UserResponse(id=3, email="cliente@gmail.com", rol=UserRole.CLIENTE, activo=True),
]


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Obtiene el listado completo de usuarios registrados (Exclusivo Admin)."
)
def list_users():
    return MOCK_USERS


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Permite registrar nuevos usuarios con roles específicos (Admin o Empleado)."
)
def create_user(user_in: UserCreate):
    return UserResponse(
        id=4,
        email=user_in.email,
        rol=user_in.rol,
        activo=user_in.activo
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Retorna el perfil y rol de un usuario en base a su identificador."
)
def get_user(user_id: int = Path(..., description="ID del usuario", ge=1)):
    return UserResponse(id=user_id, email=f"user{user_id}@comicstore.com", rol=UserRole.EMPLEADO, activo=True)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Modifica los datos de un usuario existente."
)
def update_user(user_in: UserUpdate, user_id: int = Path(..., ge=1)):
    return UserResponse(
        id=user_id,
        email=user_in.email or f"user{user_id}@comicstore.com",
        rol=user_in.rol or UserRole.EMPLEADO,
        activo=user_in.activo if user_in.activo is not None else True
    )


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    summary="Baja lógica de usuario (Soft Delete)",
    description="Desactiva a un usuario sin eliminar físicamente su historial de compras u operaciones."
)
def delete_user(user_id: int = Path(..., ge=1)):
    return UserResponse(id=user_id, email=f"user{user_id}@comicstore.com", rol=UserRole.CLIENTE, activo=False)
