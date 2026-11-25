from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from app.schemas.common import ProductType

EDITORIAL_PRODUCT_TYPES = {ProductType.MANGA, ProductType.COMIC}
COLLECTIBLE_PRODUCT_TYPES = {ProductType.FIGURA, ProductType.MERCHANDISING}
NON_NULLABLE_UPDATE_FIELDS = (
    "titulo_nombre",
    "precio_venta",
    "stock_actual",
    "tipo_producto",
    "id_franquicia",
)


def validate_product_type_requirements(
    tipo_producto: ProductType,
    id_editorial: Optional[int],
    numero_tomo: Optional[str],
    marca_fabricante: Optional[str],
) -> Optional[str]:
    """Valida campos obligatorios según la categoría del producto (US-03).

    Retorna un mensaje de error si falta un campo requerido, o None si es válido.
    """
    if tipo_producto in EDITORIAL_PRODUCT_TYPES:
        missing = []
        if id_editorial is None:
            missing.append("id_editorial")
        if not numero_tomo:
            missing.append("numero_tomo")
        if missing:
            return (
                f"Para productos de tipo '{tipo_producto.value}' son obligatorios: "
                f"{', '.join(missing)}."
            )

    if tipo_producto in COLLECTIBLE_PRODUCT_TYPES and not marca_fabricante:
        return (
            f"Para productos de tipo '{tipo_producto.value}' es obligatorio "
            "especificar 'marca_fabricante'."
        )

    return None


def _normalize_optional_str(value: Optional[str]) -> Optional[str]:
    """Convierte cadenas vacías o solo espacios en None."""
    if isinstance(value, str) and not value.strip():
        return None
    return value


class ProductBase(BaseModel):
    titulo_nombre: str = Field(..., min_length=1, max_length=255, examples=["Chainsaw Man Vol. 1"])
    descripcion: Optional[str] = Field(None, examples=["Tomo inicial de la serie de Tatsuki Fujimoto."])
    precio_venta: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2, examples=[8500.00])
    stock_actual: int = Field(0, ge=0, examples=[15])
    tipo_producto: ProductType = Field(..., examples=[ProductType.MANGA])
    id_franquicia: int = Field(..., ge=1, examples=[1])

    # Campos específicos para Manga y Cómic
    numero_tomo: Optional[str] = Field(None, max_length=50, examples=["1"])
    id_editorial: Optional[int] = Field(None, ge=1, examples=[1])
    id_demografia: Optional[int] = Field(None, ge=1, examples=[1])
    isbn: Optional[str] = Field(None, max_length=20, examples=["978-987-807-000-1"])

    # Campos específicos para Figuras y Merchandising
    marca_fabricante: Optional[str] = Field(None, max_length=100, examples=["Bandai Spirits"])

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("descripcion", "numero_tomo", "isbn", "marca_fabricante", mode="before")
    @classmethod
    def empty_str_to_none(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_str(value)


class ProductCreate(ProductBase):
    @model_validator(mode="after")
    def check_type_specific_fields(self) -> "ProductCreate":
        error = validate_product_type_requirements(
            tipo_producto=self.tipo_producto,
            id_editorial=self.id_editorial,
            numero_tomo=self.numero_tomo,
            marca_fabricante=self.marca_fabricante,
        )
        if error:
            raise ValueError(error)
        return self


class ProductUpdate(BaseModel):
    titulo_nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    precio_venta: Optional[Decimal] = Field(None, gt=0, max_digits=10, decimal_places=2)
    stock_actual: Optional[int] = Field(None, ge=0)
    tipo_producto: Optional[ProductType] = None
    id_franquicia: Optional[int] = Field(None, ge=1)
    numero_tomo: Optional[str] = Field(None, max_length=50)
    id_editorial: Optional[int] = Field(None, ge=1)
    id_demografia: Optional[int] = Field(None, ge=1)
    isbn: Optional[str] = Field(None, max_length=20)
    marca_fabricante: Optional[str] = Field(None, max_length=100)

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("descripcion", "numero_tomo", "isbn", "marca_fabricante", mode="before")
    @classmethod
    def empty_str_to_none(cls, value: Optional[str]) -> Optional[str]:
        return _normalize_optional_str(value)

    @model_validator(mode="after")
    def reject_null_on_required_fields(self) -> "ProductUpdate":
        for field_name in NON_NULLABLE_UPDATE_FIELDS:
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f"El campo '{field_name}' no puede ser nulo.")
        return self


class ProductResponse(ProductBase):
    id: int = Field(..., examples=[1])

    model_config = ConfigDict(from_attributes=True)
