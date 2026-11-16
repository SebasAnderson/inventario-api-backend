from decimal import Decimal
from typing import List, Optional
from fastapi import APIRouter, status, Path, Query, Response
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.schemas.stock import LowStockAlert
from app.schemas.common import ProductType

router = APIRouter()

MOCK_PRODUCTS = [
    ProductResponse(
        id=1,
        titulo_nombre="Chainsaw Man Vol. 1",
        descripcion="Tomo 1 de la aclamada obra de Tatsuki Fujimoto.",
        precio_venta=Decimal("8500.00"),
        stock_actual=12,
        tipo_producto=ProductType.MANGA,
        id_franquicia=1,
        numero_tomo="1",
        id_editorial=1,
        id_demografia=1,
        isbn="978-987-807-001-8",
        marca_fabricante=None
    ),
    ProductResponse(
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
        marca_fabricante=None
    ),
    ProductResponse(
        id=3,
        titulo_nombre="Figura Son Goku Super Saiyan",
        descripcion="Figura de PVC de 18 cm con peana incluida.",
        precio_venta=Decimal("45000.00"),
        stock_actual=4,
        tipo_producto=ProductType.FIGURA,
        id_franquicia=1,
        numero_tomo=None,
        id_editorial=None,
        id_demografia=None,
        isbn=None,
        marca_fabricante="Bandai Spirits"
    ),
]


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Listar y filtrar productos",
    description="Obtiene el catálogo de productos con soporte para paginación y filtros (tipo, editorial, franquicia o término de búsqueda)."
)
def list_products(
    skip: int = Query(0, ge=0, description="Número de registros a omitir para paginación"),
    limit: int = Query(20, ge=1, le=100, description="Límite de registros por página"),
    tipo_producto: Optional[ProductType] = Query(None, description="Filtrar por tipo de producto"),
    id_editorial: Optional[int] = Query(None, description="Filtrar por ID de editorial"),
    id_franquicia: Optional[int] = Query(None, description="Filtrar por ID de franquicia"),
    search: Optional[str] = Query(None, description="Buscar por título o ISBN")
):
    return MOCK_PRODUCTS


@router.get(
    "/low-stock",
    response_model=List[LowStockAlert],
    summary="Alertas de stock mínimo",
    description="Identifica y lista aquellos productos cuyo stock actual sea igual o inferior a un umbral predeterminado (por defecto 3 unidades)."
)
def get_low_stock_products(
    threshold: int = Query(3, ge=1, description="Umbral de stock mínimo de alerta")
):
    # Mock para contrato de alertas
    low_stock_item = MOCK_PRODUCTS[1]  # Batman: Año Uno con stock 2
    return [
        LowStockAlert(
            producto=low_stock_item,
            stock_actual=low_stock_item.stock_actual,
            stock_minimo_umbral=threshold,
            mensaje=f"Alerta: El stock actual ({low_stock_item.stock_actual}) es inferior o igual al umbral ({threshold})."
        )
    ]


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Dar de alta producto",
    description="Crea un nuevo producto en el catálogo validando precios mayores a cero y atributos requeridos."
)
def create_product(product_in: ProductCreate):
    return ProductResponse(
        id=4,
        **product_in.model_dump()
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Retorna el detalle completo de un artículo del catálogo."
)
def get_product(product_id: int = Path(..., ge=1)):
    return MOCK_PRODUCTS[0]


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto",
    description="Modifica los atributos, precio o descripción de un producto existente."
)
def update_product(product_in: ProductUpdate, product_id: int = Path(..., ge=1)):
    updated_data = MOCK_PRODUCTS[0].model_dump()
    for key, value in product_in.model_dump(exclude_unset=True).items():
        updated_data[key] = value
    return ProductResponse(**updated_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto del catálogo."
)
def delete_product(product_id: int = Path(..., ge=1)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
