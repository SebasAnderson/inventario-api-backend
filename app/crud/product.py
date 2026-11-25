from typing import List, Optional, Tuple
from sqlalchemy import func, or_
from sqlalchemy.orm import Query as SAQuery, Session

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.common import ProductSortBy, SortOrder
from app.schemas.product import ProductCreate, ProductFilters, ProductUpdate

SORT_COLUMN_MAP = {
    ProductSortBy.ID: Product.id,
    ProductSortBy.TITULO: Product.titulo_nombre,
    ProductSortBy.PRECIO: Product.precio_venta,
    ProductSortBy.STOCK: Product.stock_actual,
}


def _escape_like(term: str) -> str:
    return term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class ProductCRUD(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """Operaciones CRUD y búsqueda avanzada para el catálogo de productos."""

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

    def _apply_filters(self, query: SAQuery, filters: ProductFilters) -> SAQuery:
        exact_filters = [
            (Product.tipo_producto, filters.tipo_producto.value if filters.tipo_producto else None),
            (Product.id_franquicia, filters.id_franquicia),
            (Product.id_editorial, filters.id_editorial),
            (Product.id_demografia, filters.id_demografia),
        ]
        for column, value in exact_filters:
            if value is not None:
                query = query.filter(column == value)

        if filters.search:
            pattern = f"%{_escape_like(filters.search)}%"
            query = query.filter(
                or_(
                    Product.titulo_nombre.ilike(pattern, escape="\\"),
                    Product.descripcion.ilike(pattern, escape="\\"),
                    Product.isbn.ilike(pattern, escape="\\"),
                )
            )
        if filters.titulo:
            query = query.filter(Product.titulo_nombre.ilike(f"%{_escape_like(filters.titulo)}%", escape="\\"))
        if filters.isbn:
            query = query.filter(Product.isbn.ilike(f"%{_escape_like(filters.isbn)}%", escape="\\"))
        if filters.numero_tomo:
            query = query.filter(func.lower(Product.numero_tomo) == filters.numero_tomo.lower())
        if filters.precio_min is not None:
            query = query.filter(Product.precio_venta >= filters.precio_min)
        if filters.precio_max is not None:
            query = query.filter(Product.precio_venta <= filters.precio_max)
        if filters.en_stock is True:
            query = query.filter(Product.stock_actual > 0)
        elif filters.en_stock is False:
            query = query.filter(Product.stock_actual == 0)

        return query

    def search(
        self,
        db: Session,
        filters: ProductFilters,
        skip: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Product], int]:
        """Ejecuta búsqueda filtrada y devuelve (resultados_paginados, total_coincidencias)."""
        query = self._apply_filters(db.query(Product), filters)
        total = query.count()

        sort_column = SORT_COLUMN_MAP[filters.sort_by]
        primary_order = sort_column.desc() if filters.sort_order == SortOrder.DESC else sort_column.asc()
        if filters.sort_by == ProductSortBy.ID:
            query = query.order_by(primary_order)
        else:
            query = query.order_by(primary_order, Product.id.asc())

        items = query.offset(skip).limit(limit).all()
        return items, total


product = ProductCRUD(Product)
