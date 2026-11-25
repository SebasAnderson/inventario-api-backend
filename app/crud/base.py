from typing import Generic, List, Optional, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Operaciones CRUD genéricas reutilizables sobre modelos SQLAlchemy."""

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()

    def get_by_id(self, db: Session, item_id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == item_id).first()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        db.commit()
        return db_obj


class CatalogCRUD(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    """CRUD para entidades de catálogo clasificadas por nombre único."""

    def get_by_name(self, db: Session, nombre: str) -> Optional[ModelType]:
        normalized = nombre.strip().lower()
        return (
            db.query(self.model)
            .filter(func.lower(self.model.nombre) == normalized)
            .first()
        )
