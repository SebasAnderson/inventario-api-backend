from typing import List
from fastapi import APIRouter, status, Path, Response
from app.schemas.franchise import FranchiseCreate, FranchiseUpdate, FranchiseResponse

router = APIRouter()

MOCK_FRANCHISES = [
    FranchiseResponse(id=1, nombre="Dragon Ball"),
    FranchiseResponse(id=2, nombre="Naruto"),
    FranchiseResponse(id=3, nombre="Batman"),
    FranchiseResponse(id=4, nombre="Spider-Man"),
]


@router.get(
    "/",
    response_model=List[FranchiseResponse],
    summary="Listar franquicias",
    description="Retorna todas las franquicias o universos registrados."
)
def list_franchises():
    return MOCK_FRANCHISES


@router.post(
    "/",
    response_model=FranchiseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear franquicia",
    description="Registra una nueva franquicia en el catálogo."
)
def create_franchise(franchise_in: FranchiseCreate):
    return FranchiseResponse(id=5, nombre=franchise_in.nombre)


@router.get(
    "/{franchise_id}",
    response_model=FranchiseResponse,
    summary="Obtener franquicia por ID",
    description="Consulta información de una franquicia específica."
)
def get_franchise(franchise_id: int = Path(..., ge=1)):
    return FranchiseResponse(id=franchise_id, nombre="Dragon Ball")


@router.put(
    "/{franchise_id}",
    response_model=FranchiseResponse,
    summary="Actualizar franquicia",
    description="Modifica los datos de una franquicia existente."
)
def update_franchise(franchise_in: FranchiseUpdate, franchise_id: int = Path(..., ge=1)):
    return FranchiseResponse(id=franchise_id, nombre=franchise_in.nombre or "Franquicia Modificada")


@router.delete(
    "/{franchise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar franquicia",
    description="Elimina una franquicia del catálogo."
)
def delete_franchise(franchise_id: int = Path(..., ge=1)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
