from typing import List
from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.orm import Session
from app.api.v1.catalog_helpers import (
    create_catalog_item,
    delete_catalog_item,
    get_catalog_or_404,
    update_catalog_item,
)
from app.crud import demographic as crud_demographic
from app.db.session import get_db
from app.schemas.demographic import DemographicCreate, DemographicResponse, DemographicUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[DemographicResponse],
    summary="Listar demografías",
    description="Retorna la clasificación por público demográfico de los títulos.",
)
def list_demographics(
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Máximo de registros a devolver"),
    db: Session = Depends(get_db),
):
    return crud_demographic.get_all(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=DemographicResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear demografía",
    description="Agrega una nueva demografía al sistema. El nombre debe ser único.",
)
def create_demographic(demographic_in: DemographicCreate, db: Session = Depends(get_db)):
    return create_catalog_item(crud_demographic, db, demographic_in, "demografía")


@router.get(
    "/{demographic_id}",
    response_model=DemographicResponse,
    summary="Obtener demografía por ID",
    description="Consulta una demografía por su identificador.",
)
def get_demographic(demographic_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return get_catalog_or_404(crud_demographic, db, demographic_id, "Demografía")


@router.put(
    "/{demographic_id}",
    response_model=DemographicResponse,
    summary="Actualizar demografía",
    description="Modifica una demografía existente.",
)
def update_demographic(
    demographic_in: DemographicUpdate,
    demographic_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return update_catalog_item(crud_demographic, db, demographic_id, demographic_in, "Demografía", "demografía")


@router.delete(
    "/{demographic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar demografía",
    description="Elimina una demografía del catálogo. Falla si tiene productos asociados.",
)
def delete_demographic(demographic_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    delete_catalog_item(crud_demographic, db, demographic_id, "Demografía", "demografía")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
