from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.common import ProductType


class ProductBase(BaseModel):
    titulo_nombre: str = Field(..., max_length=255, examples=["Chainsaw Man Vol. 1"])
    descripcion: Optional[str] = Field(None, examples=["Tomo inicial de la serie de Tatsuki Fujimoto."])
    precio_venta: Decimal = Field(..., gt=0, decimal_places=2, examples=[8500.00])
    stock_actual: int = Field(0, ge=0, examples=[15])
    tipo_producto: ProductType = Field(..., examples=[ProductType.MANGA])
    id_franquicia: int = Field(..., examples=[1])

    # Campos específicos para Manga y Cómic
    numero_tomo: Optional[str] = Field(None, max_length=50, examples=["1"])
    id_editorial: Optional[int] = Field(None, examples=[1])
    id_demografia: Optional[int] = Field(None, examples=[1])
    isbn: Optional[str] = Field(None, max_length=20, examples=["978-987-807-000-1"])

    # Campos específicos para Figuras y Merchandising
    marca_fabricante: Optional[str] = Field(None, max_length=100, examples=["Bandai Spirits"])


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    titulo_nombre: Optional[str] = Field(None, max_length=255)
    descripcion: Optional[str] = None
    precio_venta: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_actual: Optional[int] = Field(None, ge=0)
    tipo_producto: Optional[ProductType] = None
    id_franquicia: Optional[int] = None
    numero_tomo: Optional[str] = None
    id_editorial: Optional[int] = None
    id_demografia: Optional[int] = None
    isbn: Optional[str] = None
    marca_fabricante: Optional[str] = None


class ProductResponse(ProductBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
