from typing import List
from fastapi import APIRouter, Depends, Path, Query, Response, status
from sqlalchemy.orm import Session
from app.api.v1.catalog_helpers import (
    create_catalog_item,
    delete_catalog_item,
    get_catalog_or_404,
    update_catalog_item,
)
from app.crud import publisher as crud_publisher
from app.db.session import get_db
from app.schemas.publisher import PublisherCreate, PublisherResponse, PublisherUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[PublisherResponse],
    summary="Listar editoriales",
    description="Retorna el catálogo completo de editoriales asociadas a mangas y cómics.",
)
def list_publishers(
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir"),
    limit: int = Query(100, ge=1, le=100, description="Máximo de registros a devolver"),
    db: Session = Depends(get_db),
):
    return crud_publisher.get_all(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=PublisherResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear editorial",
    description="Registra una nueva editorial en el sistema. El nombre debe ser único.",
)
def create_publisher(publisher_in: PublisherCreate, db: Session = Depends(get_db)):
    return create_catalog_item(crud_publisher, db, publisher_in, "editorial")


@router.get(
    "/{publisher_id}",
    response_model=PublisherResponse,
    summary="Obtener editorial por ID",
    description="Consulta los detalles de una editorial específica.",
)
def get_publisher(publisher_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return get_catalog_or_404(crud_publisher, db, publisher_id, "Editorial")


@router.put(
    "/{publisher_id}",
    response_model=PublisherResponse,
    summary="Actualizar editorial",
    description="Actualiza el nombre de una editorial existente.",
)
def update_publisher(
    publisher_in: PublisherUpdate,
    publisher_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    return update_catalog_item(crud_publisher, db, publisher_id, publisher_in, "Editorial", "editorial")


@router.delete(
    "/{publisher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar editorial",
    description="Elimina una editorial del sistema. Falla si tiene productos asociados.",
)
def delete_publisher(publisher_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    delete_catalog_item(crud_publisher, db, publisher_id, "Editorial", "editorial")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
