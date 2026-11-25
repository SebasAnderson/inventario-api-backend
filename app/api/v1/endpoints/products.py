from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud import (
    demographic as crud_demographic,
    franchise as crud_franchise,
    product as crud_product,
    publisher as crud_publisher,
)
from app.db.session import get_db
from app.models.product import Product
from app.schemas.common import ProductType
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    validate_product_type_requirements,
)
from app.schemas.stock import LowStockAlert

router = APIRouter()

# Mock mantenido únicamente para /low-stock hasta el Sprint 12 (Alertas de Stock Mínimo)
MOCK_LOW_STOCK_SAMPLE = ProductResponse(
    id=2,
    titulo_nombre="Batman: Año Uno",
    descripcion="Clásico del cómic norteamericano por Frank Miller.",
    precio_venta=Decimal("14500.00"),
    stock_actual=2,
    tipo_producto=ProductType.COMIC,
    id_franquicia=3,
    numero_tomo="Tomo Único",
    id_editorial=3,
    id_demografia=2,
    isbn="978-987-724-401-2",
    marca_fabricante=None,
)


def _get_product_or_404(db: Session, product_id: int) -> Product:
    db_product = crud_product.get_by_id(db, product_id)
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado.",
        )
    return db_product


def _validate_foreign_keys(
    db: Session,
    id_franquicia: int,
    id_editorial: Optional[int],
    id_demografia: Optional[int],
) -> None:
    """Verifica que las clasificaciones referenciadas existan en la base de datos."""
    checks = [
        (id_franquicia, crud_franchise, "franquicia"),
        (id_editorial, crud_publisher, "editorial"),
        (id_demografia, crud_demographic, "demografía"),
    ]
    for fk_id, crud_repo, label in checks:
        if fk_id is not None and not crud_repo.get_by_id(db, fk_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La {label} con ID {fk_id} no existe.",
            )


def _ensure_unique_isbn(
    db: Session,
    isbn: Optional[str],
    exclude_product_id: Optional[int] = None,
) -> None:
    if isbn is None:
        return
    existing = crud_product.get_by_isbn(db, isbn)
    if existing and existing.id != exclude_product_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un producto registrado con el ISBN '{isbn}'.",
        )


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Listar productos",
    description="Obtiene el catálogo de productos registrados en la base de datos con soporte para paginación básica.",
)
def list_products(
    skip: int = Query(0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(20, ge=1, le=100, description="Límite de registros por página"),
    db: Session = Depends(get_db),
):
    return crud_product.get_all(db, skip=skip, limit=limit)


@router.get(
    "/low-stock",
    response_model=List[LowStockAlert],
    summary="Alertas de stock mínimo",
    description="Identifica y lista aquellos productos cuyo stock actual sea igual o inferior a un umbral predeterminado (por defecto 3 unidades).",
)
def get_low_stock_products(
    threshold: int = Query(3, ge=1, description="Umbral de stock mínimo de alerta")
):
    # Contrato mock hasta Sprint 12
    return [
        LowStockAlert(
            producto=MOCK_LOW_STOCK_SAMPLE,
            stock_actual=MOCK_LOW_STOCK_SAMPLE.stock_actual,
            stock_minimo_umbral=threshold,
            mensaje=(
                f"Alerta: El stock actual ({MOCK_LOW_STOCK_SAMPLE.stock_actual}) "
                f"es inferior o igual al umbral ({threshold})."
            ),
        )
    ]


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dar de alta producto",
    description="Crea un nuevo producto en el catálogo validando precio positivo, ISBN único, clasificaciones válidas y campos requeridos según tipo.",
)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    _validate_foreign_keys(
        db,
        id_franquicia=product_in.id_franquicia,
        id_editorial=product_in.id_editorial,
        id_demografia=product_in.id_demografia,
    )
    _ensure_unique_isbn(db, product_in.isbn)
    try:
        return crud_product.create(db, product_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear el producto por un conflicto de integridad (ISBN duplicado o referencia inválida).",
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Retorna el detalle completo de un artículo del catálogo.",
)
def get_product(product_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return _get_product_or_404(db, product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto",
    description="Modifica los atributos, precio o detalles de un producto existente manteniendo la integridad de datos.",
)
def update_product(
    product_in: ProductUpdate,
    product_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    db_product = _get_product_or_404(db, product_id)
    updates = product_in.model_dump(exclude_unset=True)

    merged_type = updates.get("tipo_producto", ProductType(db_product.tipo_producto))
    merged_editorial = updates.get("id_editorial", db_product.id_editorial)
    merged_tomo = updates.get("numero_tomo", db_product.numero_tomo)
    merged_marca = updates.get("marca_fabricante", db_product.marca_fabricante)

    type_error = validate_product_type_requirements(
        tipo_producto=merged_type,
        id_editorial=merged_editorial,
        numero_tomo=merged_tomo,
        marca_fabricante=merged_marca,
    )
    if type_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=type_error)

    _validate_foreign_keys(
        db,
        id_franquicia=updates.get("id_franquicia", db_product.id_franquicia),
        id_editorial=merged_editorial,
        id_demografia=updates.get("id_demografia", db_product.id_demografia),
    )

    if "isbn" in updates:
        _ensure_unique_isbn(db, updates["isbn"], exclude_product_id=product_id)

    try:
        return crud_product.update(db, db_product, product_in)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el producto por un conflicto de integridad (ISBN duplicado o referencia inválida).",
        )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto del catálogo siempre que no tenga movimientos de stock registrados.",
)
def delete_product(product_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_product = _get_product_or_404(db, product_id)
    if db_product.movimientos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar un producto que tiene movimientos de stock registrados.",
        )
    try:
        crud_product.delete(db, db_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el producto porque está referenciado por otros registros.",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
