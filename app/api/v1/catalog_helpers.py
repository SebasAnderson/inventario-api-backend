from typing import Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.crud.base import CatalogCRUD


def get_catalog_or_404(crud: CatalogCRUD, db: Session, item_id: int, entity_title: str) -> Any:
    """Obtiene un registro de catálogo por ID o lanza HTTP 404."""
    db_obj = crud.get_by_id(db, item_id)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_title} con ID {item_id} no encontrada.",
        )
    return db_obj


def create_catalog_item(
    crud: CatalogCRUD,
    db: Session,
    item_in: BaseModel,
    entity_lower: str,
) -> Any:
    """Crea un registro de catálogo verificando unicidad de nombre."""
    nombre = getattr(item_in, "nombre")
    if crud.get_by_name(db, nombre=nombre):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una {entity_lower} con el nombre '{nombre}'.",
        )
    try:
        return crud.create(db, item_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una {entity_lower} con el nombre '{nombre}'.",
        )


def update_catalog_item(
    crud: CatalogCRUD,
    db: Session,
    item_id: int,
    item_in: BaseModel,
    entity_title: str,
    entity_lower: str,
) -> Any:
    """Actualiza un registro de catálogo verificando existencia y unicidad."""
    db_obj = get_catalog_or_404(crud, db, item_id, entity_title)
    nombre = getattr(item_in, "nombre", None)
    if nombre is not None:
        existing = crud.get_by_name(db, nombre=nombre)
        if existing and existing.id != item_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otra {entity_lower} con el nombre '{nombre}'.",
            )
    try:
        return crud.update(db, db_obj, item_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe otra {entity_lower} con el nombre '{nombre}'.",
        )


def delete_catalog_item(
    crud: CatalogCRUD,
    db: Session,
    item_id: int,
    entity_title: str,
    entity_lower: str,
) -> None:
    """Elimina un registro de catálogo siempre que no tenga productos asociados."""
    db_obj = get_catalog_or_404(crud, db, item_id, entity_title)
    if db_obj.productos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar una {entity_lower} que tiene productos asociados.",
        )
    try:
        crud.delete(db, db_obj)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar la {entity_lower} porque está asociada a otros registros.",
        )
