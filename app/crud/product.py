from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductCRUD(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """Operaciones CRUD para el catálogo de productos."""

    def get_by_isbn(self, db: Session, isbn: str) -> Optional[Product]:
        return db.query(Product).filter(Product.isbn == isbn.strip()).first()

    def create(self, db: Session, obj_in: ProductCreate) -> Product:
        data = obj_in.model_dump()
        data["tipo_producto"] = obj_in.tipo_producto.value
        db_obj = Product(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Product, obj_in: ProductUpdate) -> Product:
        update_data = obj_in.model_dump(exclude_unset=True)
        if "tipo_producto" in update_data and update_data["tipo_producto"] is not None:
            update_data["tipo_producto"] = update_data["tipo_producto"].value
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj


product = ProductCRUD(Product)
