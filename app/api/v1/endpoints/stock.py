from typing import List
from fastapi import APIRouter, status, Query
from app.schemas.stock import StockMovementCreate, StockMovementResponse
from app.schemas.common import StockMovementType

router = APIRouter()

MOCK_MOVEMENTS = [
    StockMovementResponse(
        id=1,
        id_producto=1,
        id_usuario=2,
        tipo_movimiento=StockMovementType.INGRESO,
        cantidad=20
    ),
    StockMovementResponse(
        id=2,
        id_producto=1,
        id_usuario=2,
        tipo_movimiento=StockMovementType.VENTA,
        cantidad=5
    ),
    StockMovementResponse(
        id=3,
        id_producto=2,
        id_usuario=1,
        tipo_movimiento=StockMovementType.AJUSTE,
        cantidad=2
    ),
]


@router.get(
    "/movements",
    response_model=List[StockMovementResponse],
    summary="Listar movimientos de inventario",
    description="Retorna el registro histórico de ingresos, ventas y ajustes de stock."
)
def list_stock_movements(
    id_producto: int = Query(None, description="Filtrar movimientos por producto específico"),
    tipo_movimiento: StockMovementType = Query(None, description="Filtrar por tipo de movimiento (Ingreso, Venta, Ajuste)")
):
    return MOCK_MOVEMENTS


@router.post(
    "/movements",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar movimiento de stock",
    description="Registra una entrada de mercadería (Ingreso), una venta o un ajuste de inventario."
)
def create_stock_movement(movement_in: StockMovementCreate):
    return StockMovementResponse(
        id=4,
        id_producto=movement_in.id_producto,
        id_usuario=2,  # Usuario operador (Mock)
        tipo_movimiento=movement_in.tipo_movimiento,
        cantidad=movement_in.cantidad
    )
