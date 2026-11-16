from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.product import Product


class Franchise(Base):
    __tablename__ = "franquicias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # Relación 1 a N: Una franquicia tiene muchos productos
    productos: Mapped[List["Product"]] = relationship("Product", back_populates="franquicia")

    def __repr__(self) -> str:
        return f"<Franchise(id={self.id}, nombre='{self.nombre}')>"
