from typing import List
from fastapi import APIRouter, status, Path, Response
from app.schemas.demographic import DemographicCreate, DemographicUpdate, DemographicResponse

router = APIRouter()

MOCK_DEMOGRAPHICS = [
    DemographicResponse(id=1, nombre="Shonen"),
    DemographicResponse(id=2, nombre="Seinen"),
    DemographicResponse(id=3, nombre="Shojo"),
    DemographicResponse(id=4, nombre="Josei"),
]


@router.get(
    "/",
    response_model=List[DemographicResponse],
    summary="Listar demografías",
    description="Retorna la clasificación por público demográfico de los títulos."
)
def list_demographics():
    return MOCK_DEMOGRAPHICS


@router.post(
    "/",
    response_model=DemographicResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear demografía",
    description="Agrega una nueva demografía al sistema."
)
def create_demographic(demographic_in: DemographicCreate):
    return DemographicResponse(id=5, nombre=demographic_in.nombre)


@router.get(
    "/{demographic_id}",
    response_model=DemographicResponse,
    summary="Obtener demografía por ID",
    description="Consulta una demografía por su identificador."
)
def get_demographic(demographic_id: int = Path(..., ge=1)):
    return DemographicResponse(id=demographic_id, nombre="Shonen")


@router.put(
    "/{demographic_id}",
    response_model=DemographicResponse,
    summary="Actualizar demografía",
    description="Modifica una demografía existente."
)
def update_demographic(demographic_in: DemographicUpdate, demographic_id: int = Path(..., ge=1)):
    return DemographicResponse(id=demographic_id, nombre=demographic_in.nombre or "Demografía Modificada")


@router.delete(
    "/{demographic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar demografía",
    description="Elimina una demografía del catálogo."
)
def delete_demographic(demographic_id: int = Path(..., ge=1)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
