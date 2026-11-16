from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import StockMovementType
from app.schemas.product import ProductResponse


class StockMovementBase(BaseModel):
    id_producto: int = Field(..., examples=[1])
    tipo_movimiento: StockMovementType = Field(..., examples=[StockMovementType.INGRESO])
    cantidad: int = Field(..., gt=0, examples=[10])


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id: int = Field(..., examples=[1])
    id_usuario: int = Field(..., examples=[2])
    fecha_movimiento: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)


class LowStockAlert(BaseModel):
    producto: ProductResponse
    stock_actual: int = Field(..., examples=[2])
    stock_minimo_umbral: int = Field(..., examples=[3])
    mensaje: str = Field(..., examples=["Stock por debajo o igual al umbral mínimo recomendado (3 unidades)."])

