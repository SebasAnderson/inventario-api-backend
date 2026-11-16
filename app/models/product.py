from decimal import Decimal
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Integer, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.franchise import Franchise
    from app.models.publisher import Publisher
    from app.models.demographic import Demographic
    from app.models.stock_movement import StockMovement


class Product(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo_nombre: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_actual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tipo_producto: Mapped[str] = mapped_column(String(50), nullable=False, index=True)

    # Clave foránea obligatoria: Franquicia
    id_franquicia: Mapped[int] = mapped_column(Integer, ForeignKey("franquicias.id"), nullable=False)

    # Claves foráneas opcionales (para Manga y Cómic)
    numero_tomo: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_editorial: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("editoriales.id"), nullable=True)
    id_demografia: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("demografias.id"), nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True, index=True)

    # Atributo opcional (para Figuras y Merchandising)
    marca_fabricante: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relaciones
    franquicia: Mapped["Franchise"] = relationship("Franchise", back_populates="productos")
    editorial: Mapped[Optional["Publisher"]] = relationship("Publisher", back_populates="productos")
    demografia: Mapped[Optional["Demographic"]] = relationship("Demographic", back_populates="productos")
    movimientos: Mapped[List["StockMovement"]] = relationship("StockMovement", back_populates="producto")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, titulo='{self.titulo_nombre}', tipo='{self.tipo_producto}')>"
