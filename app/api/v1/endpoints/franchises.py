from typing import List
from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.orm import Session
from app.api.v1.catalog_helpers import (
    create_catalog_item,
    delete_catalog_item,
    get_catalog_or_404,
    update_catalog_item,
)
from app.crud import franchise as crud_franchise
from app.db.session import get_db
from app.schemas.franchise import FranchiseCreate, FranchiseResponse, FranchiseUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[FranchiseResponse],
    summary="Listar franquicias",
    description="Retorna todas las franquicias o universos registrados.",
)
def list_franchises(
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Máximo de registros a devolver"),
    db: Session = Depends(get_db),
):
    return crud_franchise.get_all(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=FranchiseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear franquicia",
    description="Registra una nueva franquicia en el catálogo. El nombre debe ser único.",
)
def create_franchise(franchise_in: FranchiseCreate, db: Session = Depends(get_db)):
    return create_catalog_item(crud_franchise, db, franchise_in, "franquicia")


@router.get(
    "/{franchise_id}",
    response_model=FranchiseResponse,
    summary="Obtener franquicia por ID",
    description="Consulta información de una franquicia específica.",
)
def get_franchise(franchise_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return get_catalog_or_404(crud_franchise, db, franchise_id, "Franquicia")


@router.put(
    "/{franchise_id}",
    response_model=FranchiseResponse,
    summary="Actualizar franquicia",
    description="Modifica los datos de una franquicia existente.",
)
def update_franchise(
    franchise_in: FranchiseUpdate,
    franchise_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return update_catalog_item(crud_franchise, db, franchise_id, franchise_in, "Franquicia", "franquicia")


@router.delete(
    "/{franchise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar franquicia",
    description="Elimina una franquicia del catálogo. Falla si tiene productos asociados.",
)
def delete_franchise(franchise_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    delete_catalog_item(crud_franchise, db, franchise_id, "Franquicia", "franquicia")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
